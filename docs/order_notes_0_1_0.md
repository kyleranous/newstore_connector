# Order Notes
*NewStoreConnector.order_notes*

Methods for retrieving and creating Order Notes

## Available Versions
 - [0.1.0](#v0.1.0) *Default*


## v0.1.0

[NewStore Documentation](https://docs.newstore.net/api/integration/order-management/order_notes_api)

**Special Parameters**:
 - None

### Methods

#### get_order_notes
Access the [Get notes by order ID](https://docs.newstore.net/api/integration/order-management/order_notes_api#operation/showOrderNote) endpoint.

**Returns**: `requests.Response` or `dict`

**Arguments**
- order_uuid - *str* - Unique Identifier for the order IE: `f9b13b8b-1951-5b68-8aee-6f5f19be5937`
- return_json - *bool* - (*optional*) If set to `true` Only the json of the `request.Response` object will be returned. *Default*: `False`


#### create_order_note
Access the [Create order note](https://docs.newstore.net/api/integration/order-management/order_notes_api#operation/createOrderLevelNote) endpoint.

**Returns**: `requests.Response` or `dict`

**Arguments**
- order_uuid - *str* - Unique Identifier for the order IE: `f9b13b8b-1951-5b68-8aee-6f5f19be5937`
- text - *str* - The Text of the note
- source - *str* - The user ID the note is being created for
- source_type - *str* - The type of source for the note. *Default*: `integration`
- tags - *list[str]* - List of tags for the order. Requires at least 1
- return_json - *bool* - (*optional*) If set to `true` Only the json of the `request.Response` object will be returned. *Default*: `False`


#### create_item_note
Access the [Create item note](https://docs.newstore.net/api/integration/order-management/order_notes_api#operation/createItemLevelNote) endpoint.

**Returns**: `requests.Response` or `dict`

**Arguments**
 - order_uuid - *str* - Unique Identifier for the order IE: `f9b13b8b-1951-5b68-8aee-6f5f19be5937`
 - item_uuid - *str* - Unique Identifier for the product referenced in the note
 - text - *str* - The Text of the note
- source - *str* - The user ID the note is being created for
- source_type - *str* - The type of source for the note. *Default*: `integration`
- tags - *list[str]* - List of tags for the order. Requires at least 1
- return_json - *bool* - (*optional*) If set to `true` Only the json of the `request.Response` object will be returned. *Default*: `False`


#### update_note
Access the [Update note](https://docs.newstore.net/api/integration/order-management/order_notes_api#operation/updateNote) endpoint.

**Returns**: `requests.Response` or `dict`

**Arguments**
 - order_uuid - *str* - Unique Identifier for the order IE: `f9b13b8b-1951-5b68-8aee-6f5f19be5937`
 - note_uuid - *str* - Unique Identifier for the specific note being updated
 - text - *str* - The Text of the note
- source - *str* - The user ID the note is being created for
- source_type - *str* - The type of source for the note. *Default*: `integration`
- tags - *list[str]* - List of tags for the order. Requires at least 1
- return_json - *bool* - (*optional*) If set to `true` Only the json of the `request.Response` object will be returned. *Default*: `False`


#### delete_note
Access the [Delete note](https://docs.newstore.net/api/integration/order-management/order_notes_api#operation/destroyNote) endpoint.

**Returns**: `requests.Response` or `dict`

**Arguments**
 - order_uuid - *str* - Unique Identifier for the order IE: `f9b13b8b-1951-5b68-8aee-6f5f19be5937`
 - note_uuid - *str* - Unique Identifier for the specific note being deleted.
 - return_json - *bool* - (*optional*) If set to `true` Only the json of the `request.Response` object will be returned. *Default*: `False`
