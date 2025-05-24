# Inicio
> La vida es como una caja de chocolates. Nunca sabes qué te va a tocar.

KMK es una librería de software enfocada en teclados, y se usa encima de  [CircuitPython](https://circuitpython.org/). Como tal, funciona con la mayoría de [placas que soportan CircuitPython](https://circuitpython.org/downloads). KMK requiere una versión de CircuitPython 7.3 o superior.
Dispositivos ya operativos y de uso recomendado se pueden encontrar aquí: [Lista de microcontroladores oficialmente soportados](Officially_Supported_Microcontrollers.md)

## Guía de inicio rápido
> Al infinito y más allá!
1. [Instala CircuitPython 7.3 o superior](https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython). Para la mayoría de tarjetas, ha de ser tan sencillo como copiar unos archivos.
2. Obtén una copia actualizada [de KMK](https://github.com/KMKfw/kmk_firmware/archive/refs/heads/main.zip) desde la rama 'main' 
3. Descomprime el archivo y copia la carpeta `KMK` y el archivo `boot.py` en la raíz de la unidad USB correspondiente a tu placa. Suele aparecer como CIRCUITPY
4. Crea un nuevo archivo `code.py` o `main.py` en la misma raíz (al mismo nivel que boot.py) con el siguiente contenido:

***IMPORTANTE:*** Cambia los pines GP0 / GP1 por los que hayas conectado en tu teclado

```
print("Iniciando KMK")

import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation

keyboard = KMKKeyboard()

keyboard.col_pins = (board.GP0,)
keyboard.row_pins = (board.GP1,)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

keyboard.keymap = [
    [KC.A,]
]

if __name__ == '__main__':
    keyboard.go()
```

5. Con un cable (ó clip de papel) conecta ambos pines que has seleccionado para col_pin y row_pin.

![Ejemplos con las tarjetas 'feather' y 'keeboar' ](pins56.jpg)

6. Si se imprime la letra "a" (o una "Q" o ... dependiendo de tu distribución de teclado), ¡ya está!. KMK está funcionando y puedes empezar a jugar con él.

## Ahora que has empezado, puedes ir más allá...
> Esta es tu última oportunidad. Después de esto, no hay vuelta atrás. Tomas la pastilla azul: la historia termina, despiertas en tu cama y crees lo que quieras. Tomas la pastilla roja: te quedas en el país de las maravillas y te muestro qué tan profundo es el agujero de conejo. Recuerda: todo lo que ofrezco es la verdad. Nada más.

### Estas con suerte y ya tiene un teclado 100% soportado
Si tu teclado y microcontrolador están oficialmente soportados, simplemente visita la página con sus archivos y arrastralos a la raíz de su unidad flash.
Puedes encontrar el contenido en la carpeta [boards](https://github.com/KMKfw/kmk_firmware/tree/master/boards).
Necesitarás `kb.py` y `main.py`. Si necesitas instrucciones más detalladas sobre cómo personalizar la configuración y los mapeos de teclas, consulta [su documentación](config_and_keymap.md).

### Tienen otro teclado, que tú mismo hiciste, y quieres personalizar KMK para él

Primero, asegúrate de entender bien cómo funciona tu teclado. En especial la configuración de su matriz de escaneo. Puedes echar un [vistazo aquí](http://pcbheaven.com/wikipages/How_Key_Matrices_Works/) o leer la [guía](https://docs.qmk.fm/#/hand_wire) 
Una vez que lo entiendas:
- Ajusta los archivos `code.py`/`main.py`. Dirígete a [configuración y keymaps](config_and_keymap.md) y a [teclas](keys.md) respectivamente. 
- Hay una [referencia](keycodes.md) con los códigos de teclas disponibles( `keycodes`)
- La extensión [International](international.md) agrega soporte para símbolos fuera de US, y [Media Keys](media_keys.md) agrega funciones multimedia(Mutear, subir/bajar volumen, etc) 

Y para ir aún más allá:
- [Macros](macros.md) Son usados para enviar multiple caracteres consecutivamente con una sóla acción.
- [Capas/Layers](layers.md) Pueden transformar todo el funcionamiento del teclado con un solo toque 
- [HoldTap](holdtap.md) Te permite personalizar el comportamiento de una tecla, dependiendo de si es presionada un instante o presionada por más tiempo
- [TapDance](tapdance.md) Cambia el comportamiento de una tecla, dependiendo de cuántas veces consecutivas se presiona

Si deseas divertirte con características como RGB, teclados divididos y más, consulta lo que los [módulos](modules.md) y [extensiones](extensions.md) pueden hacer.
También puedes obtener buenas ideas de varios ejemplos en los [ejemplos de usuario](https://github.com/KMKfw/kmk_firmware/tree/master/user_keymaps), proveídos en nuestra [documentation](README.md).

### Precompilando KMK para tiempos de arranque más rápidos o microcontroladores con flash limitado
Este proceso genera una versión optimizada de KMK que ocupa menos espacio se carga en menos tiempo y ejecuta más rápido.
Tienes 2 opciones:
1. Compilar KMK tú mismo. Necesitarás descargar e instalar el [mpy-cross](https://adafruit-circuit-python.s3.amazonaws.com/index.html?prefix=bin/mpy-cross/)
  compatible con tu sistema operativo. No olvides añadirlo a tu PATH, prueba ejecutando `mpy-cross` desde una terminal (Powershell, Bash, Fish, etc). 
Una vez que esté configurado, ejecuta `make compile` (si tienes `make`) o `python util/compile.py` para generar las versiones `.mpy` de los archivos de KMK. Luego copia todo el directorio `kmk/` compilado a tu teclado.
Hay un par de opciones más para `make`. Usuarios experimentados puede compilar KMK y bibliotecas adicionales, y luego cargar el bytecode y el código del teclado en una sola acción:
```sh
make compile copy-compiled copy-board MPY_SOURCES='kmk/ lib/' BOARD='boards/someboard' MOUNTPOINT='/media/user/someboard'
```
2. Descarga una versión pre-compilada. Ve a [Actions > Build en la página GitHub de KMK](https://github.com/KMKfw/kmk_firmware/actions/workflows/compile.yml),
  Descarga la versión más reciente (de la rama `main`). Encontrarás un enlace de descarga al final de la página, en la sección 'Artifacts'. Descomprime la descarga y pon su contenido en la carpeta `kmk/` de tu teclado.

En ciertos microcontroladores, como el nice!nano, esto puede no ser suficiente para que KMK quepa en la memoria flash.
Empieza removiendo módulos y extensiones que no estés usando.
Empieza con `kmk/extensions`, `kmk/modules`, `kmk/quickpin`, y dejando sólo los archivos que se están cargando (Los que sí importas desde  `main.py` o `kb.py`).


## Ayuda adicional y soporte
> ¿Caminos? Adonde vamos no necesitamos... caminos .
En caso de que lo necesites, puedes encontrar ayuda de depuración en la página de [debugging](debugging.md).

Para soporte asíncrono y charlar sobre KMK, [únete a nuestra comunidad de Zulip](https://kmkfw.zulipchat.com)!

Si pides ayuda en el chat o abres un informe de error, en lo posible asegúrate de que tu copia de KMK esté actualizada.
En particular, visita y revisa el chat de Zulip *antes* de abrir un problema en GitHub sobre configuración, documentación, etc.




