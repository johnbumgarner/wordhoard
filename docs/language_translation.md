<h1><strong>Language Translation</strong></h1>
---


### Language Translation Overview

<p align="justify">
The majority of the sources that <strong>WordHoard</strong> queries are primarily in the English language. To find antonyms, synonyms, hypernyms, hyponyms and homophones for other languages <strong>WordHoard</strong> has 3 translation service modules. 
</p>

<p align="justify">
These modules support:
</p>

<ul>
	<li><a href="https://translate.google.com">Google Translate</a></li>
	<li><a href="https://www.deepl.com/translator">DeepL Translate</a></li>
	<li><a href="https://mymemory.translated.net">MyMemory Translate</a></li>
</ul>


### Google Translate

<p align="justify">
The example below uses the <i>Google Translate</i> module within <strong>WordHoard</strong> to translate Spanish language words to English language and then back into Spanish.
</p>

```python
from wordhoard import Antonyms
from wordhoard.utilities.google_translator import Translator

words = ['buena', 'contenta', 'suave']
for word in words:
    translated_word = Translator(source_language='es', 
    	                         str_to_translate=word).translate_word()
    antonyms = Antonyms(translated_word).find_antonyms()
    reverse_translations = []
    for antonym in antonyms:
        reverse_translated_word = Translator(source_language='es', 
        	                                 str_to_translate=antonym).reverse_translate()
        reverse_translations.append(reverse_translated_word)
    output_dict = {word: sorted(reverse_translations)}
    print(output_dict)
   {'buena': ['Dios espantoso', 'OK', 'abominable', 'aborrecible', 'acogedor', 
   'agravante', 'amenazante', 'angustioso', 'antiestético', 'asqueroso', 'basura', 
   'carente', 'contaminado', 'de segunda', 'decepcionante', 'defectuoso', 'deficiente', 
   'deplorable', 'deprimente', 'desagradable', 'desaliñado', 'descorazonador', 
   'desfavorecido', 'desgarbado', 'desgarrador', 'detestable', 'doloroso', 'duro', 
   'débil', 'enfermo', 'enfureciendo', 'enloquecedor', 'espantoso', 'esperado', 
   'exasperante', 'falsificado', 'falso', 'falta', 'falto', 'feo', 'frustrante', 
   'grotesco', 'horrible', 'hostil', 'impactante', 'imperfecto', 'inaceptable', 
   'inadecuado', 'inadmisible', 'inaguantable', 'incensar', 'incompetente', 
   'incongruente', 'inconsecuente', 'incorrecto', 'indeseable', 'indignante', 
   'indigno', 'indigno de', 'infeliz', 'inferior', 'infernal', 'inflamando', 
   'inmoral', 'insalubre', 'insatisfactorio', 'insignificante', 'insoportable', 
   'insuficiente', 'insufrible', 'intimidante', 'inútil', 'irreal', 'irritante', 
   'lamentable', 'lúgubre', 'maldad', 'malo', 'malvado', 'malísimo', 
   'mediocre', 'menor', 'miserable', 'molesto', 'nauseabundo', 'no a la par', 
   'no atractivo', 'no capacitado', 'no es bueno', 'no es suficiente', 'no fidedigno', 
   'no satisfactorio', 'nocivo', 'objetable', 'odioso', 'ofensiva', 'ordinario', 
   'pacotilla', 'patético', 'pecaminoso', 'perturbador', 'pobre', 'poco agraciado', 
   'poco apetecible', 'poco hermoso', 'poco imponente', 'poco satisfactorio', 
   'poco virtuoso', 'podrido', 'portarse mal', 'preocupante', 'repelente', 
   'repugnante', 'repulsivo', 'sencillo', 'significar', 'sin forma', 'sin importancia', 
   'sin placer', 'sin valor', 'sombrío', 'subóptimo', 'sucio', 'terrible', 'triste', 
   'trágico', 'vicioso', 'vil']}
   
   truncated...
```

### Deep Translate

<p align="justify">
The example below uses the <i>Deep Translate</i> module within <strong>WordHoard</strong> to translate Spanish language words to English language and then back into Spanish.
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

### MyMemory Translate

<p align="justify">
The example below uses the <i>MyMemory Translate</i> module within <strong>WordHoard</strong> to translate Spanish language words to English language and then back into Spanish.
</p>

```python
from wordhoard import Antonyms
from wordhoard.utilities.mymemory_translator import Translator

words = ['buena', 'contenta', 'suave']
for word in words:
    translated_word = Translator(source_language='es', 
                                 str_to_translate=word,
                                 email_address='your_email_address').translate_word()
    antonyms = Antonyms(translated_word).find_antonyms()
    reverse_translations = []
    for antonym in antonyms:
        reverse_translated_word = Translator(source_language='es', 
                                             str_to_translate=antonym,
                                             email_address='your_email_address').reverse_translate()
        reverse_translations.append(reverse_translated_word)
    output_dict = {word: sorted(set(reverse_translations))}
    print(output_dict)
    {'buena': ['abominable', 'aborrecible', 'aceptar', 'afligido', 'agravante', 
    'amenazante', 'ansia nauseosa', 'antiestético', 'asco', 'asqueroso', 'atroz', 
    'basura', 'caballo que padece tiro', 'carente', 'chocante', 'consternador', 
    'de baja calidad', 'decepcionando', 'defectuoso', 'deficiente', 'deprimentes', 
    'desagradable', 'desaliñado', 'descorazonador', 'desfavorecido', 'desgarbado', 
    'desgarrador', 'desgraciado', 'detestable', 'dios espantoso', 'doloroso', 
    'duelo psicológico', 'débil', 'enfermas', 'enfermo', 'enfureciendo', 'enloquecedor', 
    'es lo suficientemente buena', 'espantoso', 'esperado', 'está por el suelo', 
    'exasperante', 'fake', 'familiar', 'feo', 'forjado', 'fúnebre', 'grutesco', 
    'horrible', 'hostil', 'impropio', 'inaceptable', 'inadecuado', 'inadmisible', 
    'inaguantable', 'incensar', 'incomible', 'incompetente', 'incongruente', 
    'indeseable', 'indignante', 'indigno', 'inexperto', 'infeliz', 'inferior', 
    'infernal', 'inflamando', 'inmoral', 'inquietante', 'insatisfactorio', 
    'insignificante', 'insoportable', 'insuficientes', 'insufrible', 'insípido', 
    'intimidante', 'intrascendente', 'irreal', 'irritante', 'lamentable', 'lúgubre', 
    'mal', 'mal acogido', 'malo', 'media', 'mezquino', 'molesto', 'nauseabundo', 
    'no es bueno', 'no satisfactorio', 'no útil', 'nocivo', 'o antipatico', 'odioso', 
    'ofensivo', 'parcialmente podrido', 'patético', 'pecador', 'penoso', 'pequeños', 
    'perturbador', 'piojoso', 'poco agraciado', 'poco apetecible', 'poco atractivo', 
    'poco fiable', 'poco hermoso', 'poco imponente', 'poco satisfactorio', 'poco virtuoso', 
    'podrido', 'portarse mal', 'preocupante', 'pretérito imperfecto', 'puede ser frustrante', 
    'querer', 'repelente', 'repugnante', 'repulsivo', 'residuos de lana', 'riling', 
    'ser agrupado con', 'simple', 'sin forma', 'sin importancia', 'sin placer', 'sin valor', 
    'sombría', 'subóptimo', 'sucio', 'tarifa segunda', 'temperatura', 'terrible', 
    'triste', 'trágico', 'tu bienvenida mi hermano', 'un error', 'vano', 'vicioso', 
    'vil', '¡horrible', 'áspero']}
    
    truncated... 
```

<p align="justify">
It is worth noting that none of the translation services are perfect, thus it can make <i>“lost in translation”</i> mistakes. These mistakes are usually related to the translation service not having an in-depth understanding of the language or not being able to under the context of these words being translated.  In some cases there will be nonsensical literal translations.  So any translations should be reviewed for these common mistakes. 
</p>