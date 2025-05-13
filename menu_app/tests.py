from django.test import TestCase, RequestFactory
from django.template import Context, Template
from django.urls import reverse
from menu_app.models import MenuItem


class TreeMenuFunctionalityTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        # Строим тестовое меню с вложенностью
        # A
        # ├── B
        # │   ├── D
        # │   └── E
        # └── C

        self.a = MenuItem.objects.create(name='A', menu_name='test_menu', url='/a/')
        self.b = MenuItem.objects.create(name='B', menu_name='test_menu', url='/a/b/', parent=self.a)
        self.c = MenuItem.objects.create(name='C', menu_name='test_menu', url='/a/c/', parent=self.a)
        self.d = MenuItem.objects.create(name='D', menu_name='test_menu', url='/a/b/d/', parent=self.b)
        self.e = MenuItem.objects.create(name='E', menu_name='test_menu', url='/a/b/e/', parent=self.b)

    def render_menu(self, path='/', menu_name='test_menu'):
        request = self.factory.get(path)
        context = Context({'request': request})
        template = Template(f"{{% load menu_tags %}}{{% draw_menu '{menu_name}' %}}")
        return template.render(context)

    def test_menu_renders_top_level(self):
        html = self.render_menu('/a/')
        self.assertIn('A', html)
        self.assertIn('B', html)
        self.assertIn('C', html)

    def test_active_item_is_highlighted(self):
        html = self.render_menu('/a/b/e/')
        self.assertIn('class="active"', html)
        self.assertIn('E', html)

    def test_parent_chain_is_expanded(self):
        html = self.render_menu('/a/b/d/')
        self.assertIn('B', html)
        self.assertIn('D', html)
        self.assertIn('A', html)

    def test_subitems_hidden_if_not_active(self):
        html = self.render_menu('/a/')
        self.assertIn('B', html)
        self.assertNotIn('D', html)
        self.assertNotIn('E', html)

    def test_only_one_db_query(self):
        with self.assertNumQueries(1):
            self.render_menu('/a/b/')

    def test_position_autofill(self):
        # Создаем пункт без указания позиции
        item = MenuItem.objects.create(name='Z', menu_name='test_menu', url='/z/')
        self.assertGreater(item.position, 0)

    def test_named_url_resolution(self):
        MenuItem.objects.create(name='Named', menu_name='test_menu', named_url='home')
        html = self.render_menu(reverse('home'))
        self.assertIn('Named', html)
        self.assertIn('href="/"', html)

    def test_menu_isolated_by_name(self):
        MenuItem.objects.create(name='Other', menu_name='another_menu', url='/other/')
        html = self.render_menu(menu_name='test_menu')
        self.assertIn('A', html)
        self.assertNotIn('Other', html)
