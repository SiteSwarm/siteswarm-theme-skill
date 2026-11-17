# Dataset queries and pagination

## Contents

- [Check runtime support](#check-runtime-support)
- [Query the complete mounted dataset](#query-the-complete-mounted-dataset)
- [Choose equality, membership, or saved criteria](#choose-equality-membership-or-saved-criteria)
- [Paginate rows and navigation separately](#paginate-rows-and-navigation-separately)
- [Keep related-record queries bounded](#keep-related-record-queries-bounded)
- [Verify with representative data](#verify-with-representative-data)

## Check runtime support

Use the behavior below only on a server and preview runtime that support
query-backed datasets and independent pagination controls. Confirm support in
the target environment before relying on these features. Updating this skill
or client does not upgrade a hosted server or the client's preview image.
Older runtimes may filter only an initial 200-row window or reject newer syntax.
A successful small local preview cannot prove complete hosted query results.

## Query the complete mounted dataset

Access a mounted dataset as `datasets.services`, not `datasets.services.records`.
On a compatible server, supported operations query the complete mounted scope
before loading rows. They retain the mount's existing restrictions.

| Operation | Result |
| --- | --- |
| Direct `for` | At most 200 matching rows, even with `limit: 1000` |
| `for ... offset: 200 limit: 20` | Reach later matches without loading earlier rows |
| `.size`, `.length`, `.count`, or `\| size` | Complete query count without loading records |
| `.materialized_size` | Direct iteration count, at most 200 |
| `.first` / `.last` | First or last query result; load one row |
| `{% paginate query by 20 %}` | Count the complete query and load one page |
| `.all_records` | Explicitly load every matching row into memory |

Build queries before loading rows. `where`, `sort`, `sort_natural`, `reverse`,
`slice`, and `map` remain lazy on mounted datasets. Counts include slices.
Operation order matters: `slice: 0, 10 | where: 'active', true` searches those
ten rows; `where: 'active', true | slice: 0, 10` selects ten active rows.

```liquid
{% assign active_services = datasets.services | where: 'active', true | sort: 'title' %}
<p>{{ active_services | size }} services</p>
{% paginate active_services by 20 as rows %}
  {% for entry in rows %}
    {% render 'service-card', entry: entry %}
  {% endfor %}
  {% render 'pagination', pagination: pagination %}
{% endpaginate %}
```

Sort and filter records before `map`. A projection keeps one value per row,
including nulls. Projected values support indexing such as `names[250]` and
`names[-1]`, and Liquid `contains` over the complete scoped query; explicit
slices constrain membership. Direct projected output, `join`, and `json` are
bounded to 200 values. Do not treat them as full-dataset exports.

Ordinary sorting uses stored types: integer fields sort numerically, while
numbers stored as strings sort lexicographically. Use `sort_natural` for
case-insensitive text ordering.

Apply `uniq`, `compact`, `reject`, `find`, `find_index`, `has`, `concat`, and `sum`
to a page array or explicit `.all_records`. Applying them directly to a lazy
dataset raises a Liquid error rather than silently processing a partial set.
After materialization, ordinary array counts describe only that array.

Query stored fields and schema aliases. Computed record `id`, `_item_url`,
`_mount_path`, and resolved attachment properties require explicit array
processing. Prefer stored keys and page-sized operations to loading all rows.

## Choose equality, membership, or saved criteria

Use ordinary `where: 'field', value` for typed equality: numeric `5` differs
from string `'5'`, and an array does not equal one of its elements. An omitted
or nil target selects truthy values, excluding only missing/null and `false`.
Legacy `count_where` compares scalar text, including numeric-to-string coercion;
it remains efficient but does not test array membership.

Use exact typed membership for array-valued fields:

```liquid
{% assign garden_services = datasets.services | where_contains: 'category_slugs', 'garden' %}
{{ datasets.services | count_contains: 'category_slugs', 'garden' }}
```

Use `dataset_filter: field, operator, value` for saved-filter criteria. Supported
operators are `eq`, `neq`, `contains`, `gt`, `gte`, `lt`, `lte`, `in`, `null`,
`not_null`, and `array_contains`. Here `eq`/`neq` compare scalar text;
`contains` is a case-sensitive substring match; `array_contains` tests exact
typed membership. Numeric comparisons accept numeric strings; invalid record
values do not match and invalid targets raise an error.

```liquid
{% assign rated = datasets.services | dataset_filter: 'rating', 'gte', 4 %}
{% assign featured = rated | dataset_view: 'Featured' %}
```

Use a saved view's name or `view_...` ID. If SiteSwarm MCP is connected, obtain
it with `list_dataset_views` or `get_dataset_view`. A view must belong to the
mounted dataset. Selection intersects existing mount restrictions and prior
criteria; inline criteria and attached reusable filters combine with AND.
Missing views or views from another dataset raise an error.

## Paginate rows and navigation separately

| Context | Rows | Navigation |
| --- | --- | --- |
| Mounted collection route | `collection` | `pagination` |
| Inside a `paginate` block | `paginate.collection` or its `as` alias | `pagination` |

Never iterate `pagination.collection`; it does not exist. Pass
`pagination: pagination` explicitly into isolated render snippets. The starter
includes [a navigation snippet](../assets/starter/snippets/pagination.liquid).
Use `pagination.parts` for numbered links rather than iterating every page.
Each part exposes `title`, `url`, `is_current`, and `is_link`.

Use this block syntax:

```liquid
{% assign per = settings.per_page | default: 20 %}
{% paginate datasets.services by per as service_rows %}
  {% for entry in service_rows %}
    {% render 'service-card', entry: entry %}
  {% endfor %}
  {% render 'pagination', pagination: pagination %}
{% endpaginate %}
{% paginate datasets.reviews by 10 as review_rows page_param: 'reviews_page' %}
  {% for review in review_rows %}<p>{{ review.text | escape }}</p>{% endfor %}
  {% render 'pagination', pagination: pagination %}
{% endpaginate %}
```

Resolve page size to an integer or decimal-digit string from 1 through 10,000.
Literal sizes, variables, and lookups such as `settings['per_page']` are valid.
Missing, zero, negative, fractional, boolean, and oversized values raise an
error before rows load. Assign filter or arithmetic results first; inline
filters and arithmetic in tag options are unsupported. Prefer modest page sizes.

The first block follows `?page=N`. The second follows `?reviews_page=N` and
starts at page 1 if that parameter is absent. Use a different `page_param` for
each independently controlled list. Names start with a letter or underscore,
followed by letters, digits, underscores, or hyphens. Add `page: 1` to hold a
block on page 1. If both options are set, `page:` selects the page and
`page_param:` controls navigation URLs. Both accept literals or lookups.

Pages below 1 normalize to 1; pages beyond the end clamp to the last page.
An empty or missing collection has zero rows, page 1 of 1, and no links.
Links retain unrelated query values, nested filters, and other lists' page
parameters. A page-1 link removes only the current block's parameter. These
controls retain query values; they do not implement search or filtering.
Nested blocks restore outer pagination objects and aliases when they finish.

## Keep related-record queries bounded

Match the stable foreign key actually stored on both datasets:

```liquid
{% assign reviews = datasets.reviews | where: 'service_key', item.service_key %}
<p>{{ reviews | size }} reviews</p>
{% paginate reviews by 10 as review_rows page_param: 'reviews_page' %}
  {% for review in review_rows %}<p>{{ review.text | escape }}</p>{% endfor %}
  {% render 'pagination', pagination: pagination %}
{% endpaginate %}
```

Use a stored canonical ID, slug, or other stable business key. A displayed
SiteSwarm `id` is a generated prefix ID; do not assume it equals an imported
record's canonical ID. There is no automatic dataset join. Avoid loading every
review inside each card loop. Per-card queries also multiply work; prefer
lookups on detail pages or denormalized common card fields. Reserve
`.all_records` for intentional, acceptably small full-set processing.

## Verify with representative data

With authorization for the target staging site:

1. Use more than 200 fictional records with known matches after row 200.
2. Compare full counts, empty results, late-row matches, and ordered pages.
3. Check numeric/string/false equality and exact array membership.
4. Verify offsets after row 200 and both slice/filter orders.
5. Verify saved-view intersection and rejection of another dataset's view.
6. Exercise two independent lists, variable sizes, page 1, excessive page
   numbers, retained query values, and navigation rendered through a snippet.
7. Check related lookups on representative volumes and observe latency or
   query counts where available. Do not claim scalability from a tiny fixture.

Report the actual runtime and checks performed. Static validation and mock
preview do not establish hosted query correctness or deployment support.
