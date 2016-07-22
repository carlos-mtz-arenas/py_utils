# this scripts describes how to display images within an html/text content on django

###############################################################################
###############################################################################

# Models should be like this:


class ImagePost(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField('image', upload_to='posts/gallery', null=True, blank=True)

    def __unicode__(self):
        return self.name

# post
class Post(models.Model):
    # who created the post
    user = models.ForeignKey(YourUserModel)
    # post stuff
    title = models.CharField(max_length=300, null=False)
    content = models.TextField(null=False)
    creation_date = models.DateTimeField(default=now)
    last_modified = models.DateTimeField(default=now)

    # INFO: define the images as they are on a separate attribute, this will be marged into the text/HTML later
    images = models.ManyToManyField(ImagePost, blank=True)

    def __unicode__(self):
        return '%s - %s' % (self.user, self.title)

    @property
    def content_html(self):
        '''
          This is just a property that will be called on the template section and will contain the tokens
          replaced by the proper html img component with their proper url!
          the usage will be as follows:
            - When creating the html, for each image you want to display, use ![image_name] to be displayed, where image_name is the name
                of the file
        '''
        actual_content = self.content
        all_images = self.images.all()

        # execute only for those posts that actually contain an image
        if all_images is None or len(all_images) == 0:
            return actual_content

        names = []
        for image in all_images:
            image_url = image.image.url
            name = '![%s]' % image.name.lower()
            # gather the token ![image_name] into a list
            names.append({'name': image.name, 'url': transform_media_link(image_url, name)})
        # replace all image names tokens within the same self.content
        for name in names:
            actual_content = transform_body(name['name'], name['url'], actual_content)
        return actual_content

###############################################################################
###############################################################################

# then on your utils or wherever you want to keep it...

# helpers for image gallery usage on Post, Event, and News elements
def transform_body(name, url, content):
    return re.sub(r'\!\[%s\]' % name, url, content)

def transform_media_link(url, name):
    return re.sub(r'\!\[(.*)\]', r'<img src=%s />' % url, name)

###############################################################################
###############################################################################

# then, finally on the template, we just do the following to display it:

'''
{{post.content_html|safe|linebreaks}}
'''

# insights
# * yeap kind of looks ugly, but, hey! it works :P
# * when exposing this to a REST service, you may want to call the *safe and linebreaks* functions manually so that it will be safe
