<h1><strong>MyMemory translator</strong></h1>
---

<p align="justify">
The example below uses the <i>MyMemory Translator</i> module within <strong>WordHoard</strong> to translate Spanish language words to English language and then back into Spanish.
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
