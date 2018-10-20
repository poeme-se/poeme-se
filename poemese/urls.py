from django.conf.urls import url
from poemese import views
from django.views.generic import TemplateView

app_name = 'poemese'

urlpatterns = [

    # Url's de Login/Logout/Cadastro
    url(r'^signin/$', views.sign_in, name='sign_in'),
    url(r'^signup/$', views.sign_up, name='sign_up'),
    url(r'^signout/', views.deslogar, name='deslogar'),

    # Url's de Poema
    url(r'^$', views.read_poema, name='poemas'),
    url(r'^escrever/$', views.create_poema, name='novo_poema'),
    url(r'^atualizar/(?P<id>\d+)$', views.update_poema, name='atualizar_poema'),
    url(r'^excluir/(?P<pk>\d+)$', views.delete_poema, name='deletar_poema'),
    url(r'^carregarMaisPoemas/$', views.loadMorePoems, name='carregarMaisPoemas'),
    url(r'^addLike/$', views.addLike, name='addLike'),

    url(r'^addComment/$', views.addComment, name='addComment'),
    url(r'^loadComments/$', views.loadComments, name='loadComments'),

    url(r'^addSuggestion/$', views.addSuggestion, name="add_suggestion"),
    url(r'^loadSuggestion/$', views.loadSuggestions, name="load_suggestion"),

    # Url's das pesquisas
    url(r'search_works/$', views.search_works_view, name='searchWorks'),
    url(r'search_friends/$', views.search_friends_view, name='searchFriends'),

    # Url's de Usuário
    url(r'^perfil/(?P<pseudonimo>[\w-]+)/$', views.perfil, name='perfil'),
    url(r'^followList/(?P<name>[\w-]+)/$', views.followList, name='followList'),
    url(r'^listaPoemas/(?P<name>[\w-]+)/$', views.poemList, name='poemList'),
    # url(r'^listaGrupos/(?P<name>[\w-]+)/$', views.groupList, name='groupList'),
    url(r'^obras/$', views.bookList, name='bookList'),
    url(r'^follow/$', views.follow_friend_view, name='follow'),

    url(r'^listaGrupos/$', views.groupList, name='groupList'),
    # url(r'^listaGrupos/(?P<name>[\w-]+)/$', views.group, name='group'),

    url(r'^settings/$', views.config, name="config"),

    # Url's de Erro
    url(r'^404/$', TemplateView.as_view(template_name="404.html")),
    url(r'^500/$', TemplateView.as_view(template_name="500.html"))
]
