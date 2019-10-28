
For a Django implementation (which uses this library) see https://github.com/Amsterdam/django-audit-log

# DataPunt Audit Log

DataPunt Audit Log is a simple python package that provides a simple way
to allow for uniform audit logs across all our applications. 

The AuditLogger class can be provided with info and will log to stdout. 

Eventually this logger wil run inside our docker containers. Filebeat
will be used to read the audit logs from those containers, and will send 
them along to logstash, which in turn sends them to elastic. 


## Quick start

1. Install using pip

    ```bash
    pip install audit_log
    ```
   
2. Add logs to your code

   ```python
    AuditLogger()\
        .set_http_request(method='GET', url='https://localhost', user_agent='Test')\
        .info('This is a log message')\
        .send_log()
    ```
   

## Basic Usage

The audit log is simple in its usage. There are several methods to set context-info
regarding the request:

```python
set_http_request(self, method: str, url: str, user_agent: str = '') -> 'AuditLogger'
set_http_response(self, status_code: int, reason: str, headers: dict = None) -> 'AuditLogger'
set_user(self, authenticated: bool, provider: str, email: str, roles: list = None, ip: str = '', realm: str = '') -> 'AuditLogger'
set_filter(self, object_name: str, fields: str, terms: str) -> 'AuditLogger'
set_results(self, results: list = None) -> 'AuditLogger'
```

Also, a log message and loglevel can be provided to indicate what the request is actually doing. 
This is done by calling one of the following methods:

```python
debug(self, msg: str) -> 'AuditLogger'
info(self, msg: str) -> 'AuditLogger'
warning(self, msg: str) -> 'AuditLogger'
error(self, msg: str) -> 'AuditLogger'
critical(self, msg: str) -> 'AuditLogger'
```

Note that each of these methods returns `self`. We use an adaption of the builder pattern here to 
make the logger simple in use. It enables us to do:

```python
AuditLogger()\
    .set_http_request(method='GET', url='https://localhost', user_agent='Test')\
    .info('This is a log message')\
    .send_log()
```


## Context info

Although none of the methods are required before sending the log (you could even send an empty log), 
you are strongly urged to add as much info as possible before sending the log. This will
eventually result in a complete audit log that contains the necessary details to perform proper 
auditing.


### HTTP request
`AuditLogger().set_http_request(self, method: str, url: str, user_agent: str = '')` allows to 
provide more info about the HTTP request that has been executed.

This method will add the following details to the log:

```json
"http_request": {
    "method": "get|post|head|options|etc..",
    "url": "https://datapunt.amsterdam.nl",
    "user_agent": "full browser user agent"
},
```

### HTTP response
`AuditLogger().set_http_response(self, status_code: int, reason: str, headers: dict = None)` allows
to provide more info detailing the HTTP response that was returned to the user. 

This method will add the following details to the log:

```json
"http_response": {
    "status_code": "http status code",
    "reason": "http status reason",
    "headers": {
      "key": "value"
}
```


### User
`AuditLogger().set_user(self, authenticated: bool, provider: str, email: str, roles: list = None, ip: str = '', realm: str = '')`
allows to provide details regarding the user that executed a specific request.

This method will add the following details to the log:

```json
"user": {
    "authenticated": "True/False",
    "provider": "auth backend the user authenticated with",
    "realm": "optional realm when using keycloak or another provider",
    "email": "email of logged in user",
    "roles": "roles attached to the logged in user",
    "ip": "ip address"
}
```

### Filter 
`AuditLogger().set_filter(self, object_name: str, fields: str, terms: str)` allows to provide
info on the requested type of object and the filters that have been used  (a user searches 
for 'terms', which are matched on specific 'fields' of the 'object').

This method will add the following details to the log:

```json
"filter": {
    "object": "Object name that is requested",
    "fields": "Fields that are being filtered on, if applicable",
    "terms": "Search terms, if applicable"
}
```

### Results
`AuditLogger().set_results(self, results: list)` allows to store what results have been returned 
to the user. 

It is up to the developer to decide whether the amount of data that would be added here will 
become a burden instead of a blessing.

This method will add the following details to the log:

```json
"results": {
    ...
  }
```
