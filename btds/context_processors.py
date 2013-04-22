from btds.forms import *

def AddForms(request):
    NAF = NovelAddForm()
    VAF = VolumeAddForm()
    MAF = MetaAddForm()
    LAF = LinkAddForm()
    AAF = AuthorAddForm()
    IAF = IllustratorAddForm()
    TAF = TranslatorAddForm()
    EAF = EditorAddForm()
    LANGAF = LanguageAddForm()
    PAF = PublisherAddForm()
    GAF = GenreAddForm()
    FAF = FormatAddForm()
    IMGAF = ImageAddForm()
    #return {'Novel':NAF,'Volume':VAF,'Meta':MAF,'Link':LAF,'Author':AAF,'Illustrator':IAF,'Translator':TAF,'Editor':EAF,'Language':LANGAF,'Publischer':PAF,'Genre':GAF,'Format':FAF,'Image':IMGAF}
    return {'NAF':NAF,'VAF':VAF,'MAF':MAF,'LAF':LAF,'AAF':AAF,'IAF':IAF,'TAF':TAF,'EAF':EAF,'LANGAF':LANGAF,'PAF':PAF,'GAF':GAF,'FAF':FAF,'IMGAF':IMGAF}

def BTDSAC(request):
    if request.user.is_superuser:
        is_god = True
    else:
        is_god = False
    if request.user.groups.filter(name='Admin'):
        is_mortal = True
    else:
        is_mortal = False
    return {'is_god':is_god,'is_mortal':is_mortal}