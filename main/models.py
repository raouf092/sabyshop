from django.db import models
class Order(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='orders/', blank=True, null=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    titre = models.CharField(max_length=255)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    couleur = models.CharField(max_length=100, blank=True, null=True)  # ✅ AJOUTER

    publie = models.BooleanField(default=False)

    def __str__(self):
        return self.titre

class Commande(models.Model):
    date_commande = models.DateTimeField(auto_now_add=True)
    nom = models.CharField(max_length=100, blank=True, null=True)
    prenom = models.CharField(max_length=100, blank=True, null=True)
    adresse = models.TextField(blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Commande #{self.id} - {self.nom}"


class LigneCommande(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name="lignes")
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    quantite = models.IntegerField(default=1)
    taille = models.CharField(max_length=50, blank=True, null=True)  # ✅ ajoute la taille


class CommandeImage(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='commandes/')

    def __str__(self):
        return f"Image pour {self.commande}"
