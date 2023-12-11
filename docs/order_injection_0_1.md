# Order Injection
*NewStoreConnector.order_injection*

Methods for injecting Orders into NewStore

## Available Versions
 - [0.1](#v_0.1) *Default*


## v 0.1

[NewStore Documentation](https://docs.newstore.net/api/integration/order-management/order_injection_api)

**Special Parameters**:
 - None

### Methods

#### create_order
Accesses the [Create order](https://docs.newstore.net/api/integration/order-management/order_injection_api#operation/CreateOrder) endpoint. 

Returns: `requests.Response` or `dict`

**Arguments**
- payload - *dict* - Order payload to be injected into NewStore
- skip_validation - *bool* - (*optional*) Set to `True` to skip the build in validation. If `False` and `payload` fails validaiton, a `ValueError` is raised with a dictionary of all the failures the payload has. *Default*: `False`
- return_json - *bool* - (*optional*) If set to `true` Only the json of the `request.Response` object will be returned. *Default*: `False`

#### validate_create_order_payload
Conducts validation on the Order injection Payload for [create_order](#create_order).

Returns: `RuleSet`
*RuleSet documentation can be found [here](https://github.com/kyleranous/api_toolkit/blob/main/docs/validate.md#ruleset).*

**Arguments**
- payload - *dict* - Order payload to be validated