

def main():
    fake = Faker()

    for i in range(30):
        post = Post.objects.create(
            title=fake.unique.text(),
            slug=slugify(fake.text()),
            content=fake.text(),
        )
        print(f"Created posts. title: {post.title}")

    post_count = Post.objects.count()

    print(f"There are {post_count} posts in the database")

    posts = Post.objects.all()
    print(f"There are {posts.count()} posts in the database")


if __name__ == "__main__":
    import os

    from django.core.wsgi import get_wsgi_application

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
    application = get_wsgi_application()

    from django.template.defaultfilters import slugify
    import random
    from faker import Faker
    from blog.models import Post

    main()
