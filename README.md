# Blog

## Usage

### Email settings
Edit src/core/settings.py for email notifications

```python
EMAIL_BACKEND = ''
EMAIL_HOST = ''
EMAIL_PORT = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = ''
EMAIL_USE_SSL = ''
```
### Build docker and create admin account
Run in Blog/
> docker-compose run web python src/manage.py createsuperuser

### Run application
> docker-compose up
