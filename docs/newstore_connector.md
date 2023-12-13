# NewStore Connector
## TOC
 - [Classes](#classes)
   - [NewStoreConnector](#NewStoreConnector)
 - [Modules](#modules)
## Classes

### NewStoreConnector
`NewStoreConnector` is the primary interface class to the NewStore API's. It extends [APIConnector](https://github.com/kyleranous/api_toolkit/blob/main/docs/connector.md).

`NewStoreConnector` Handles the authentication and access to the API Modules. All API Modules can be accessed through `NewStoreConnector`

#### Attributes

 - tenant - *str* - The tenant being accessed IE: `fictionaltenant` or `fictionaltenant-staging`
 - env - *str* - The Environment being accessed, *Default*: `p`
 - client_id - *str* - The Client Id used to access the NewStore API's. See Note 1
 - client_secret - *str* - The Secret used with the Client ID  to access the NewStore API's. *See Note 1*
 - role - *str* - The role used for the NewStore API Session. *Default*: `iam:providers:read`. *See Note 1*
 - token - *str* - Used in place of `client_id`, `client_secret`, `role` for authentication. *See Note 2*

 **Notes**
 1. NewStore Authentication [Documentation](https://docs.p.newstore.partners/#/http/getting-started/newstore-rest-api/getting-started/authorization)
 2. If using an external authentication manager, instead of sending `client_id`, `client_secret` and `role`, a NewStore Bearer Token can be passed to the `token` attribute.

 **Optional Attributes**
 NewStoreConnector extends `api_toolkit.connector.ApiConnector`. [Documentation](https://github.com/kyleranous/api_toolkit/blob/main/docs/connector.md)

 The following attributes relate to automatic retries from the session connections and have default values. *Note* Automatic retries are defaulted to disabled. Enable Automatic retries by setting `max_retries >= 1`.
 - max_retries - *int* - Maximum number of times to attempt retries. *Default*: `0`
 - backoff_factor - *int* or *float* - Used to calculate time between subsequent retries. See [Backoff Factor](#backoff-factor)
 - status_forcelist - *list[int]* - HTTP Status' that a retry should be attempted for. *Default*: `[408, 413, 429, 500, 502, 503, 504, 521, 522, 524]`
 *Note*: Do not allow retries on HTTP Status Code `403` when connecting to NewStore. that is the status code used when rate limited and it could delay the time until the client is unblocked.
 - allowed_methods - *list[str]* - List of methods that allow retries. *Default*: `['HEAD', 'GET', 'PUT', 'DELETE', 'OPTIONS', 'TRACE', 'POST', 'PATCH']`


#### Backoff Factor
The Backoff Factor is used to calculate the time between retries in seconds. 
```
backoff_factor * (2 ** (number_of_retries - 1))
```
If the backoff factor is set to `2` and max retries is set to `5`:
| Retry Number | Calculation | Delay Time(s) |
| :----------: | :---------: | :-----------: |
| 1            | 2*2^(0-1)   | 1             |
| 2            | 2*2^(1-1)   | 2             |
| 3            | 2*2^(2-1)   | 4             |
| 4            | 2*2^(3-1)   | 8             |
| 5            | 2*2^(4-2)   | 16            |

If it took 5 seconds for each request to get a response back from the server the total time the request would take is:
```
5s + 1s + 5s + 2s + 5s + 4s + 5s + 8s + 5s + 16s + 5s = 61s
```
Keep this in mind when configuring retry settings.


## Modules
Modules are used for access specific NewStore API Groups. `NewStoreConnector` Handles the management of the modules and will import the approriate modules at the time it is called. Each Module documentation contains a list of the available versions for each module, and indicates the default version that will be loaded if no version is specified. 

### Setting The Module Version
To set a specific version of a module (When available)
```python
>>> from newstore_connector import NewStoreConnector
>>>
>>> auth_creds = {...}
>>> ns_conn = NewStoreConnector(**auth_creds)
>>> # View the default customer_profile API Version
>>> ns_conn.customer_profile.api_version
"2.0.0"
>>> # Set customer_profile to use API V1.0.0
>>> ns_conn.customer_profile = "1.0.0"
>>> ns_conn.customer_profile.api_version
"1.0.0"
>>>
```

### Modules
 - [Order Injection](order_injection_0_1.md) `NewStoreConnector.order_injection` - Access to API's for Order Injection into NewStore
 - [Order Notes](order_notes_0_1_0.md) `NewStoreConnector.order_notes` - Access to NewStore Order Notes API