easyui-menu
===========

django项目，使用easyui，动态菜单的项目


Quict start
------------
1. pip install easyui
2. Add "easyui" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'polls',
    )

2. Include the easyui URLconf in your project urls.py like this::

    url(r'^easyui/', include('easyui.urls', namespace='easyui')),

3. Run `python manage.py migrate` to create the polls models.

4. Visit http://127.0.0.1:8000/easyui/menu/ to see the base menu.
