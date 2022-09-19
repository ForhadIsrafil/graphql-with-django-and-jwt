import graphene
from graphene_django import DjangoObjectType
from .models import Post
from django.template.defaultfilters import slugify
from .schema2 import Query as Query2

class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = ("id", "title", "content", "published")


class Query(Query2):
    posts = graphene.List(PostType)
    post_search = graphene.List(PostType, search=graphene.String())

    @graphene.resolve_only_args # can add decorator for resolver on latest package of graphql
    def resolve_posts(self):
        return Post.objects.all().order_by('-id')

    def resolve_post_search(self, info, search):
        return Post.objects.filter(title__icontains=search)


class PostMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)

    post = graphene.Field(PostType)

    @classmethod
    def mutate(cls, self, info, title, content):
        post = Post(title=title, content=content, slug=slugify(title))
        post.save()
        return PostMutation(post=post)


class UpdatePost(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        title = graphene.String(required=True)
        content = graphene.String(required=True)

    post = graphene.Field(PostType)

    @classmethod
    def mutate(cls, self, info, id, title, content):
        post = Post.objects.filter(id=id).first()
        if post is not None:
            post.title = title
            post.slug = slugify(title)
            post.content = content
            post.save()
            return UpdatePost(post=post)
        else:
            return UpdatePost(post=post)


class DeletePost(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    msg = graphene.String()
    status = graphene.Boolean(default_value=True)

    @classmethod
    def mutate(cls, self, info, id):
        if Post.objects.filter(id=id).first():
            post = Post.objects.get(id=id).delete()
            return DeletePost(msg="Post deleted Successfully", status=True)
        else:
            return DeletePost(msg="Post not found.", status=False)


class Mutation(graphene.ObjectType):
    create_new_post = PostMutation.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
