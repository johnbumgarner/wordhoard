<h1><strong>Google Translator</strong></h1>
---

<p align="justify">
The example below uses the <i>Google Translator</i> module within <strong>WordHoard</strong> to translate Spanish language words to English language and then back into Spanish.
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

