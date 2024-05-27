<h1 style="color:IndianRed;"><strong>DeepL Translator</strong></h1>

---

<p align="justify">
The example below uses the <i>DeepL Translator</i> module within <strong>WordHoard</strong> to translate Spanish language words to English language and then back into Spanish.
</p>

```python
from wordhoard import Antonyms
from wordhoard.utilities.deep_translator import Translator

words = ['buena', 'contenta', 'suave']
for word in words:
    translated_word = Translator(source_language='es', 
    	                         str_to_translate=word,
                                 api_key='your_api_key').translate_word()
    antonyms = Antonyms(translated_word).find_antonyms()
    reverse_translations = []
    for antonym in antonyms:
        reverse_translated_word = Translator(source_language='es', 
        	                                 str_to_translate=antonym,
                                             api_key='your_api_key').reverse_translate()
        reverse_translations.append(reverse_translated_word)
    output_dict = {word: sorted(set(reverse_translations))}
    print(output_dict)
    {'buena': ['abominable', 'agravante', 'angustia', 'antiestético', 'antipático', 
    'asqueroso', 'basura', 'casero', 'contaminado', 'crummy', 'de mala calidad', 
    'de segunda categoría', 'decepcionante', 'defectuoso', 'deficiente', 'deplorable', 
    'deprimente', 'desagradable', 'descorazonador', 'desgarrador', 'detestable', 'dios-horrible', 
    'doloroso', 'duro', 'débil', 'en llamas', 'enfermo', 'enfureciendo a', 'enloquecedor', 
    'equivocada', 'espantoso', 'esperado', 'exasperante', 'falso', 'falta', 'feo', 'forjado', 
    'frumpish', 'frumpy', 'frustrante', 'grotesco', 'horrible', 'hostil', 'impactante', 
    'imperfecto', 'impermisible', 'inaceptable', 'inadecuado', 'inadmisible', 'incandescente', 
    'incompetente', 'incongruente', 'indeseable', 'indignante', 'indigno', 'infeliz', 'inferior', 
    'infernal', 'inflamando', 'inmoral', 'inquietante', 'insalubre', 'insatisfactorio', 
    'insignificante', 'insoportable', 'insostenible', 'insuficiente', 'insufrible', 
    'intimidante', 'intrascendente', 'irreal', 'irritante', 'lamentable', 'llano', 
    'lúgubre', 'mal', 'mal favorecido', 'malvado', 'media', 'mediocre', 'menor', 'miserable', 
    'molestos', 'nauseabundo', 'no apto', 'no cualificado', 'no es agradable', 'no es bienvenido', 
    'no es bueno', 'no es lo suficientemente bueno', 'no es sano', 'no está a la altura', 
    'no hay que olvidar que', 'no se puede confiar en', 'nocivo', 'objetable', 'odioso', 
    'ofensiva', 'ok', 'ordinario', 'patético', 'pecaminoso', 'perturbando', 'pobre', 
    'poco apetecible', 'poco atractivo', 'poco encantador', 'poco imponente', 'poco útil', 
    'podrido', 'problemático', 'prohibiendo', 'pésimo', 'que molesta', 'queriendo', 
    'rankling', 'repelente', 'repugnante', 'repulsivo', 'rilando', 'se comportan mal', 
    'sin alegría', 'sin duda', 'sin forma', 'sin importancia', 'sin placer', 'sin pretensiones', 
    'sin sentido', 'sin valor', 'sombrío', 'subestándar', 'subóptima', 'terrible', 'triste', 
    'trágico', 'uncute', 'unvirtuoso', 'vicioso', 'vil', 'yukky']}
    
    truncated...
```

