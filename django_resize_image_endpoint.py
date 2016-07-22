
@login_required
@require_http_methods(['POST'])
def update_user_image(request):
    form = UpdateImageProfileForm(request.POST, request.FILES)
    data = {'status': 'success'}
    if form.is_valid():
        LOGGER.info('trying to update profile picture')
        try:
            (filename, image) = _resize_image(form.cleaned_data.get('profile_picture'))
            user = SEIUser.objects.get(id=request.user.id)
            user.avatar.save(filename, image)
            if (user.avatar is not None):
                data['url'] = user.avatar.url
        except:
            LOGGER.error('error while trying to update profile picture for user ' + request.user.username)
    else:
        data = {'status': 'danger', 'message': 'Archivo inválido'}
    return JsonResponse(data, safe=False)


def _resize_image(external_image):
    # scale dimensions
    image_file = StringIO.StringIO(external_image.read())

    image = Image.open(image_file)

    resized_image = image.resize(
        scale_dimensions(image.size[0], image.size[1]))

    image_file = StringIO.StringIO()
    resized_image.save(image_file, 'JPEG', quality=90)


    filename = hashlib.md5(image_file.getvalue()).hexdigest()+'.jpg'
    fullpath = os.path.join('/tmp', filename)

    thumbnail_file = open(fullpath, 'w')
    resized_image.save(thumbnail_file, 'JPEG')
    thumbnail_file = open(fullpath, 'r')
    content = File(thumbnail_file)

    return (filename, content)

