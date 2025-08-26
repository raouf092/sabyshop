import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import Article, Commande, CommandeImage, LigneCommande

def is_staff_user(user):
    return user.is_staff

# Page d'accueil avec la liste des articles
def home(request):
    articles = Article.objects.filter(publie=True)
    return render(request, 'main/home.html', {'articles': articles})

# Formulaire de commande
def commande(request):
    if request.method == "POST":
        Article.objects.get_or_create(
            id=1,
            defaults={
                'titre': 'Chemise Manches Courtes Oversize Imprimée',
                'prix': 29.99,
                'publie': True
            }
        )
        
        nouvelle_commande = Commande.objects.create(
            nom=request.POST.get("nom"),
            prenom=request.POST.get("prenom"),
            adresse=request.POST.get("adresse"),
            telephone=request.POST.get("telephone"),
        )

        cart_data = request.POST.get("cart_data")
        
        if cart_data:
            try:
                panier = json.loads(cart_data)
                for item in panier:
                    article_id = item.get("id")
                    try:
                        article = Article.objects.get(id=article_id)
                        quantite = item.get("quantity", 1)
                        taille = item.get("size", "")
                        
                        LigneCommande.objects.create(
                            commande=nouvelle_commande,
                            article=article,
                            quantite=quantite,
                            taille=taille
                        )
                    except Article.DoesNotExist:
                        continue
            except json.JSONDecodeError:
                pass

        return redirect("/")

    return render(request, "main/commande.html")

# Liste des commandes
def ord(request):
    commandes = Commande.objects.all()
    return render(request, "main/ord.html", {"commandes": commandes})

# ✅ Page de détails article
def orders(request, id):
    article = get_object_or_404(Article, id=id)
    return render(request, "main/orders.html", {"article": article})

def ajouter_article(request):
    if request.method == 'POST':
        titre = request.POST.get('titre')
        prix = request.POST.get('prix')
        couleur = request.POST.get('couleur')  # ✅ AJOUTER
        image = request.FILES.get('image')
        publie = bool(request.POST.get('publie'))

        Article.objects.create(
            titre=titre,
            prix=prix,
            couleur=couleur,  # ✅ AJOUTER
            image=image,
            publie=publie
        )
        return redirect('home')

    return render(request, 'main/ajouter_article.html')
# Supprimer un article
def delete_article(request, id):
    article = get_object_or_404(Article, id=id)
    article.delete()
    return redirect('home')

# Ajouter des images à une commande
def ajouter_images_commande(request, id):
    commande = get_object_or_404(Commande, id=id)
    if request.method == 'POST':
        for fichier in request.FILES.getlist('images'):
            CommandeImage.objects.create(commande=commande, image=fichier)
        return redirect('orders', id=commande.id)
    return render(request, 'main/ajouter_images_commande.html', {'commande': commande})
