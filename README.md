# Blog

## Usage

### Email settings
Edit these lines in src/core/settings.py for email notifications

```python
EMAIL_HOST = ''
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
```
### Build docker and create admin account
Run in Blog/
> docker-compose up
Stop service after everything is running

> 'Ctr'+ C

Create superuser
> docker-compose run web python src/manage.py createsuperuser

### Run application
> docker-compose up
