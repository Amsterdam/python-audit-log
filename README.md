

# DataPunt Audit Log

DataPunt Audit Log is a simple Django app that will log all incoming requests
and their corresponding responses to a configurable endpoint. 

During the process request phase, the logger is attached to the request. Before 
returning a response the app can easily provide extra context. In the process
response phase the auditlog middleware will send the log. 


## Quick start

1. Install using pip

    ```bash
    pip install datapunt_auditlog
    ```
   
2. Add "datapunt_auditlog" to your INSTALLED_APPS:

    ```python
    INSTALLED_APPS = [
        ...
        'datapunt_auditlog',
    ]
    ```

3. Add the AuditLogMiddleware to your MIDDLEWARE:

    ```python
    MIDDLEWARE = [
        ...
       'audit_log.middleware.AuditLogMiddleware',
    ]
    ```

4. Set the AUDIT_LOG_APP_NAME in the settings.py. This will identify the 
   app and make it recognisable in the logs. Also specify the 
   AUDIT_LOG_LOGSTASH_HOST and AUDIT_LOG_LOGSTASH_PORT. This is where the 
   logs will be written to.
    ```python
    AUDIT_LOG_APP_NAME = os.getenv('AUDIT_LOG_APP_NAME')
    AUDIT_LOG_LOGSTASH_HOST = os.getenv('AUDIT_LOG_APP_NAME')
    AUDIT_LOG_LOGSTASH_PORT = os.getenv('AUDIT_LOG_APP_NAME')
    ```

At this point all requests/responses will be logged. For providing extra context
(which you are strongly urged to do so), see next chapters.

## Default context info

By default the audit log sends the following json structure per request:

```json
{
  "app": {
    "name": "AUDIT_LOG_APP_NAME"
  },
  "http_request": {
    "method": "get|post|head|options|etc..",
    "url": "https://datapunt.amsterdam.nl?including=querystring",
    "user_agent": "full browser user agent"
  },
  "http_response": {
    "status_code": "http status code",
    "reason": "http status reason",
    "headers": {
      "key": "value"
    }
  },
  "user": {
    "authenticated": "True/False",
    "provider": "auth backend the user authenticated with",
    "realm": "optional realm when using keycloak or another provider",
    "email": "email of logged in user",
    "roles": "roles attached to the logged in user",
    "ip": "ip address"
  }
}
```
    
Each json entry is set by its corresponding method. In this case, 
the middleware sets them automatically by calling
`set_app_name()`, `set_http_request()` and `set_user_fom_request()` 
in the process_request method. In the process_response method the
last data is set by invoking `set_http_response()`.

After the response has been processed the middleware automatically
creates the log item by calling `send_log()`. 
    
## Custom optional context info

Per request it is possible to add optional context info. For a complete
audit log, you are strongly urged to add more info inside your view.

Adding extra context is quite simple. The auditlog object has been added
to the request by the middleware. Therefore every view can simply access 
it via the request object.

### Filter 
`AuditLog.set_filter(self, object_name, fields, terms)` allows to provide
info on the requested type of object and the filters that have been used 
(a user searches for 'terms', which are matched on specific 'fields' of the 
'object').

This method will add the following details to the log:

```json
"filter": {
      "object": "Object name that is requested",
      "fields": "Fields that are being filtered on, if applicable",
      "terms": "Search terms, if applicable"
  }
```

### Results
`AuditLog.set_results(self, results)` allows to pass a json dict
detailing exactly what results have been returned to the user. 

It is up to the developer to decide whether the amount of 
data that would be added here will become a burden instead
of a blessing.

This method will add the following details to the log:

```json
"results": {
    ...
  }
```

### Message and loglevel
At last, a log message and loglevel can be provided to indicate 
what the request is actually doing. This is done by calling 
one of the following methods:

```python
AuditLog.debug(self, msg)
AuditLog.info(self, msg)
AuditLog.warning(self, msg)
AuditLog.error(self, msg)
AuditLog.critical(self, msg)
```
    
These methods will add the following details to the log:

```json
"type": "DEBUG|INFO|WARNING|ERROR|etc",
"message": "log message"
```
