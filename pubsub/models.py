from django.db import models


class Entity(models.Model):
    entity_id = models.IntegerField(primary_key=True)
    jid = models.CharField(max_length=999)

    class Meta:
        db_table = 'entities'


class Node(models.Model):
    node_id = models.IntegerField(primary_key=True)
    node = models.CharField(max_length=999)
    node_type = models.CharField(max_length=999)
    collection = models.CharField(max_length=999)
    persist_items = models.BooleanField()
    deliver_payloads = models.BooleanField()
    send_last_published_item = models.CharField(max_length=999)

    class Meta:
        db_table = 'nodes'


class Affiliation(models.Model):
    affiliation_id = models.IntegerField(primary_key=True)
    entity = models.ForeignKey(Entity)
    node = models.ForeignKey(Node)
    affiliation = models.CharField(max_length=999)

    class Meta:
        db_table = 'affiliations'


class Subscription(models.Model):
    subscription_id = models.IntegerField(primary_key=True)
    entity = models.ForeignKey(Entity)
    resource = models.TextField(max_length=999)
    node = models.ForeignKey('nodes.Node')
    state = models.TextField(max_length=999)
    subscription_type = models.TextField(max_length=999)
    subscription_depth = models.TextField(max_length=999)

    class Meta:
        db_table = 'subscriptions'


class Items(models.Model):
    item_id = models.IntegerField(primary_key=True)
    node = models.ForeignKey(Node)
    item = models.CharField(max_length=999)
    publisher = models.CharField(max_length=999)
    data = models.CharField(max_length=9999)
    date = models.DateField()

    class Meta:
        db_table = 'items'
