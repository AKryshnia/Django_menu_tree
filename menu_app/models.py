from django.db import models
from django.urls import reverse, NoReverseMatch


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    menu_name = models.CharField(max_length=100)
    url = models.CharField(max_length=200, blank=True)
    named_url = models.CharField(max_length=100, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    position = models.PositiveIntegerField(default=0, blank=True)
    
    def save(self, *args, **kwargs):
        self.menu_name = self.menu_name.strip().lower()
        if self.position == 0:
            siblings = MenuItem.objects.filter(
                menu_name=self.menu_name,
                parent=self.parent
            )
            self.position = siblings.count() + 1
        super().save(*args, **kwargs)
        
    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.name

    def get_url(self):
        if self.named_url:
            try:
                return reverse(self.named_url)
            except NoReverseMatch:
                pass
        return self.url or '#'
