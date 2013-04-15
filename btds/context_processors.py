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
    return {'NAF':NAF,'VAF':VAF,'MAF':MAF,'LAF':LAF,'AAF':AAF,'IAF':IAF,'TAF':TAF,'EAF':EAF,'LANGAF':LANGAF,'PAF':PAF,'GAF':GAF,'FAF':FAF,'IMGAF':IMGAF}