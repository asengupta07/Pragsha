import akismet
from django.conf import settings


def is_spam(request, comment_content):
    akismet_api_key = settings.AKISMET_API_KEY
    akismet_blog_url = settings.AKISMET_BLOG_URL

    try:
        akismet_api = akismet.Akismet(
            akismet_api_key,
            blog_url=akismet_blog_url
        )

        akismet_api.verify_key()

        return akismet_api.comment_check(
            user_ip=request.META['REMOTE_ADDR'],
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            comment_content=comment_content,
        )
    except akismet.AkismetError:
        # Handle any errors with Akismet API, e.g., log or return False
        return False
