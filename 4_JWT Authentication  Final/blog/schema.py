import graphene
from graphene_django import DjangoObjectType
from .models import Post
from django.template.defaultfilters import slugify
from graphql_auth.schema import MeQuery, UserQuery
from graphql_auth import mutations


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = ('id', 'title', 'content')


class Query(UserQuery, MeQuery, graphene.ObjectType):
    posts = graphene.List(PostType)
    post_search = graphene.List(PostType, search=graphene.String())

    def resolve_posts(self, info):
        return Post.objects.all()

    def resolve_post_search(self, info, search):
        return Post.objects.filter(title__icontains=search)


class PostMutation(graphene.Mutation):
    __doc__ = "Update a specific post"

    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)

    post = graphene.Field(PostType)

    @classmethod
    def mutate(cls, self, info, title, content):
        post = Post(title=title, content=content, slug=slugify(title))
        post.save()
        return PostMuatation(post=post)


class UpdatePost(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        title = graphene.String(required=True)
        content = graphene.String(required=True)

    post = graphene.Field(PostType)

    @classmethod
    def mutate(cls, self, info, id, title, content):
        post = Post.objects.get(id=id)
        post.title = title
        post.slug = slugify(title)
        post.content = content
        post.save()
        return UpdatePost(post=post)


class DeletePost(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    msg = graphene.String()
    status = graphene.Boolean(default_value=True)

    @classmethod
    def mutate(cls, self, info, id):
        post = Post.objects.get(id=id).delete()
        return DeletePost(msg="Post deleted Successfully", status=True)


class Mutation(graphene.ObjectType):
    create_new_post = PostMutation.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()
    user_registration = mutations.Register.Field()
    user_verification = mutations.VerifyAccount.Field()
    user_authentication = mutations.ObtainJSONWebToken.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
