# Importar as bibliotecas necessárias
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Definir a letra da Ave Maria em latim
text = """
Ave Maria, gratia plena,
Dominus tecum.
Benedicta tu in mulieribus,
Et benedictus fructus ventris tui, Iesus.

Sancta Maria, Mater Dei,
Ora pro nobis peccatoribus,
Nunc et in hora mortis nostrae. Amen.
"""

# Criar um mapa de palavra com a letra da Ave Maria
wordcloud = WordCloud().generate(text)

# Mostrar o mapa de palavra usando o matplotlib
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
