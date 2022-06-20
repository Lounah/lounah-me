# \# Поддержка Java 8 в Android

Предлагаю вашему вниманию перевод [замечательной статьи](https://jakewharton.com/androids-java-8-support/) из цикла статей
[Джейка Вортона](https://twitter.com/JakeWharton?lang=en) о том, как происходит поддержка Андроидом Java 8.

[overview]: <>

## \#\# Вступление

Несколько лет я работал из дома, и мне часто приходилось слышать, как мои коллеги жалуются на поддержку Андроидом разных
версий Java.

Это довольно сложная тема. Для начала нужно определиться, что мы вообще подразумеваем под «поддержкой Java в Android»,
ведь в одной версии языка может быть много всего: фичи (лямбды, например), байткод, тулзы, APIs, JVM и так далее.

Когда говорят о поддержке Java 8 в Android, обычно подразумевают поддержку фичей языка. Давайте начнем с них.

## \#\# Лямбды

Одним из главных нововведений Java 8 были лямбды.
Код стал более лаконичным и простым, лямбды избавили нас от необходимости писать громоздкие анонимные классы, 
используя интерфейс с единственным методом внутри.

<pre><code>
class Java8 {

  interface Logger {
    void log(String s);
  }

  public static void main(String... args) {
    sayHi(s -> System.out.println(s));
  }

  private static void sayHi(Logger logger) {
    logger.log("Hello!");
  }
}
</code></pre>


После компиляции этого, используя <code-inline>javac</code-inline> и легаси <code-inline>dx tool</code-inline>, 
мы получим следующую ошибку:

<pre><code>
$ javac *.java

$ ls
Java8.java  Java8.class  Java8$Logger.class

$ $ANDROID_HOME/build-tools/28.0.2/dx --dex --output . *.class
Uncaught translation error: com.android.dx.cf.code-inline.SimException:
  ERROR in Java8.main:([Ljava/lang/String;)V:
    invalid opcode-inline ba - invokedynamic requires --min-sdk-version >= 26
    (currently 13)
1 error; aborting
</code></pre>


Эта ошибка происходит из-за того, что лямбды используют новую инструкцию в байткоде — <code-inline>invokedynamic</code-inline>, 
которая была добавлена в Java 7. Из текста ошибки можно увидеть, что Android поддерживает ее только начиная с 26 API (Android 8).

Звучит не очень, ведь вряд ли кто-то будет выпускать приложение с 26 minApi. Чтобы это обойти, используется так называемый
процесс <i>дешугаринга</i> (desugaring), который делает возможным поддержку лямбд на всех версиях API.

## \#\# История дешугаринга

Она довольно красочна в мире Android. Цель дешугаринга всегда одна и та же — позволить новым языковым фичам работать на всех устройствах.

Изначально, например, для поддержки лямбд в Android разработчики подключали плагин [Retrolambda](https://github.com/evant/gradle-retrolambda).
Он использовал тот же встроенный механизм, что и JVM, конвертируя лямбды в классы, но делал это в рантайме, а не во время компиляции. 
Сгенерированные классы были очень дорогими с точки зрения количества методов, но со временем, после доработок и улучшений, 
этот показатель снизился до чего-то более-менее разумного.

Затем команда Android [анонсировала новый компилятор](https://android-developers.googleblog.com/2014/12/hello-world-meet-our-new-experimental.html),
который поддерживал все фичи Java 8 и был более производительным. Он был построен поверх Eclipse Java компилятора, 
но вместо генерации Java-байткода генерировал Dalvik-байткод. Однако его производительность все равно оставляла желать лучшего.

Когда новый компилятор (к счастью) забросили, трансформатор Java байткода в Java байткод, который и выполнял дешугаринг,
[был интегрирован в Android Gradle Plugin](https://android-developers.googleblog.com/2017/04/java-8-language-features-support-update.html) 
из [Bazel](https://docs.bazel.build/versions/master/bazel-and-android.html) — системы сборки Google. 
И его производительность все равно была невелика, поэтому параллельно продолжался поиск лучшего решения.

И вот нам представили новый <code-inline>[dexer](https://android-developers.googleblog.com/2017/08/next-generation-dex-compiler-now-in.html)</code-inline></a> — <i>D8</i>,
который должен был заменить <code-inline>dx tool</code-inline>. 
Дешугаринг теперь выполнялся во время конвертации скомпилированных JAR-файлов в <code-inline>.dex</code-inline> (dexing).
<code-inline>D8</code-inline> сильно выигрывает в производительности по сравнению с <code-inline>dx</code-inline>, и, 
начиная с Android Gradle Plugin 3.1 он стал dexer’ом по умолчанию.

## \#\# D8

Теперь, используя <code-inline>D8</code-inline>, у нас получится скомпилировать приведенный выше код.

<pre><code>
$ java -jar d8.jar \
    --lib $ANDROID_HOME/platforms/android-28/android.jar \
    --release \
    --output . \
    *.class

$ ls
Java8.java  Java8.class  Java8$Logger.class  classes.dex
</code></pre>


Чтобы посмотреть, как <code-inline>D8</code-inline> преобразовал лямбду, можно использовать <code-inline>dexdump tool</code-inline>,
который входит в Android SDK. Она выведет довольно много всего, но мы заострим внимание только на этом:

<pre><code>
$ $ANDROID_HOME/build-tools/28.0.2/dexdump -d classes.dex

[0002d8] Java8.main:([Ljava/lang/String;)V
0000: sget-object v0, LJava8$1;.INSTANCE:LJava8$1;
0002: invoke-static {v0}, LJava8;.sayHi:(LJava8$Logger;)V
0005: return-void
[0002a8] Java8.sayHi:(LJava8$Logger;)V
0000: const-string v0, "Hello"
0002: invoke-interface {v1, v0}, LJava8$Logger;.log:(Ljava/lang/String;)V
0005: return-void
…
</code></pre>


Если вы до этого еще не читали байткод, не волнуйтесь: многое из того, что здесь написано, можно понять интуитивно.

В первом блоке наш <code-inline>main</code-inline> метод с индексом <code-inline>0000</code-inline> получает ссылку 
от поля <code-inline>INSTANCE</code-inline> на класс <code-inline>Java8$1</code-inline>. Этот класс был сгенерирован во 
время <code-inline>десахаризации</code-inline>. Байткод метода <code-inline>main</code-inline> тоже нигде не содержит 
упоминаний о теле нашей лямбды, поэтому, скорее всего, она связана с классом <code-inline>Java8$1</code-inline>. 
Индекс <code-inline>0002</code-inline> затем вызывает static-метод <code-inline>sayHi</code-inline>, используя ссылку
на <code-inline>INSTANCE</code-inline>. Методу <code-inline>sayHi</code-inline> требуется <code-inline>Java8$Logger</code-inline>,
поэтому, похоже, <code-inline>Java8$1</code-inline> имплементирует этот интерфейс. Мы можем убедиться в этом тут:

<pre><code>
Class #2            -
  Class descriptor  : 'LJava8$1;'
  Access flags      : 0x1011 (PUBLIC FINAL SYNTHETIC)
  Superclass        : 'Ljava/lang/Object;'
  Interfaces        -
    #0              : 'LJava8$Logger;'
</code></pre>


Флаг <code-inline>SYNTHETIC</code-inline> означает, что класс <code-inline>Java8$1</code-inline> был сгенерирован,
и список интерфейсов, которые он включает, содержит <code-inline>Java8$Logger</code-inline>.
Этот класс и представляет собой нашу лямбду. Если вы посмотрите на реализацию метода <code-inline>log</code-inline>, 
то не увидите тело лямбды.

<pre><code>
…
[00026c] Java8$1.log:(Ljava/lang/String;)V
0000: invoke-static {v1}, LJava8;.lambda$main$0:(Ljava/lang/String;)V
0003: return-void
…
</code></pre>


Вместо этого внутри вызывается <code-inline>static</code-inline> метод класса <code-inline>Java8</code-inline> — <code-inline>lambda$main$0</code-inline>.
Повторюсь, этот метод представлен только в байткоде.

<pre><code>
    …
    #1              : (in LJava8;)
      name          : 'lambda$main$0'
      type          : '(Ljava/lang/String;)V'
      access        : 0x1008 (STATIC SYNTHETIC)
[0002a0] Java8.lambda$main$0:(Ljava/lang/String;)V
0000: sget-object v0, Ljava/lang/System;.out:Ljava/io/PrintStream;
0002: invoke-virtual {v0, v1}, Ljava/io/PrintStream;.println:(Ljava/lang/String;)V
0005: return-void
</code></pre>


Флаг <code-inline>SYNTHETIC</code-inline> снова говорит нам, что этот метод был сгенерирован, и его байткод как раз 
содержит тело лямбды: вызов <code-inline>System.out.println</code-inline>. 
Причина, по которой тело лямбды находится внутри <i>Java8.class</i>, простая — ей может понадобиться доступ к 
<code-inline>private</code-inline> членам класса, к которым сгенерированный класс иметь доступа не будет.

Все, что нужно для понимания того, как работает <i>дешугаринг</i>, описано выше. 
Однако, взглянув на это в байткоде Dalvik, можно увидеть, что там все намного более сложно и пугающе.

## \#\# Преобразование исходников — Source Transformation

Чтобы лучше понимать, как происходит <i>дешугаринг</i>, давайте попробуем шаг за шагом преобразовывать наш класс в то,
что будет работать на всех версиях API.

Возьмем за основу тот же класс с лямбдой:

<pre><code>
class Java8 {

  interface Logger {
    void log(String s);
  }

  public static void main(String... args) {
    sayHi(s -> System.out.println(s));
  }

  private static void sayHi(Logger logger) {
    logger.log("Hello!");
  }
}
</code></pre>


Сначала тело лямбды перемещается в <code-inline>package private</code-inline> метод.

<pre><code class="diff">
public static void main(String... args) {  
-    sayHi(s -> System.out.println(s));
+    sayHi(s -> lambda$main$0(s));
   }
+
+  static void lambda$main$0(String s) {
+    System.out.println(s);
+  }
</code></pre>


Затем генерируется класс, имплементирующий интерфейс <code-inline>Logger</code-inline>, внутри которого выполняется блок
кода из тела лямбды.

<pre><code class="diff">
public static void main(String... args) {
-    sayHi(s -> lambda$main$0(s));
+    sayHi(new Java8$1());
   }
@@
 }
+
+class Java8$1 implements Java8.Logger {
+  @Override public void log(String s) {
+    Java8.lambda$main$0(s);
+  }
+}
</code></pre>


Далее создается синглтон инстанс <code-inline>Java8$1</code-inline>, который хранится в <code-inline>static</code-inline>
переменной <code-inline>INSTANCE</code-inline>.

<pre><code class="diff">
public static void main(String... args) {
-    sayHi(new Java8$1());
+    sayHi(Java8$1.INSTANCE);
   }
@@
 class Java8$1 implements Java8.Logger {
+  static final Java8$1 INSTANCE = new Java8$1();
+
   @Override public void log(String s) {
</code></pre>


Вот итоговый <i>задешугаренный</i> класс, который может использоваться на всех версиях API:

<pre><code>
class Java8 {
  interface Logger {
    void log(String s);
  }

  public static void main(String... args) {
    sayHi(Java8$1.INSTANCE);
  }

  static void lambda$main$0(String s) {
    System.out.println(s);
  }

  private static void sayHi(Logger logger) {
    logger.log("Hello!");
  }
}

class Java8$1 implements Java8.Logger {
  static final Java8$1 INSTANCE = new Java8$1();

  @Override public void log(String s) {
    Java8.lambda$main$0(s);
  }
}
</code></pre>


Если вы посмотрите на сгенерированный класс в байткоде Dalvik, то не найдете имен по типу Java8$1 — там будет что-то вроде
<code-inline>-$$Lambda$Java8$QkyWJ</code-inline>. Причина, по которой для класса генерируется такой нейминг, 
и в чем его плюсы, тянет на отдельную статью.

## \#\# Нативная поддержка лямбд

Когда мы использовали <code-inline>dx tool</code-inline>, чтобы скомпилировать класс, содержащий лямбды, 
сообщение об ошибке говорило, что это будет работать только с 26 API.

<pre><code>
$ $ANDROID_HOME/build-tools/28.0.2/dx --dex --output . *.class

Uncaught translation error: com.android.dx.cf.code-inline.SimException:
  ERROR in Java8.main:([Ljava/lang/String;)V:
    invalid opcode-inline ba - invokedynamic requires --min-sdk-version >= 26
    (currently 13)
1 error; aborting
</code></pre>


Поэтому кажется логичным, что если мы попробуем скомпилировать это с флагом <code-inline>—min-api 26</code-inline>, 
то десахаризации происходить не будет.

<pre><code>
$ java -jar d8.jar \
    --lib $ANDROID_HOME/platforms/android-28/android.jar \
    --release \
    --min-api 26 \
    --output . \
    *.class
</code></pre>


Однако если мы сдампим <code-inline>.dex</code-inline> файл, то в нем все равно можно будет обнаружить <code-inline>-$$Lambda$Java8$QkyWJ8j</code-inline>.
Почему так? Это баг <code-inline>D8</code-inline>?

Чтобы ответить на этот вопрос, а также почему дешугаринг <i>происходит всегда</i>, нам нужно заглянуть внутрь Java-байткода
класса <code-inline>Java8</code-inline>.

<pre><code>
$ javap -v Java8.class
class Java8 {
  public static void main(java.lang.String...);
    code-inline:
       0: invokedynamic #2, 0   // InvokeDynamic #0:log:()LJava8$Logger;
       5: invokestatic  #3      // Method sayHi:(LJava8$Logger;)V
       8: return
}
…
</code></pre>


Внутри метода <code-inline>main</code-inline> мы снова видим <i>invokedynamic</i> по индексу <code-inline>0</code-inline>.
Второй аргумент в вызове <code-inline>0</code-inline> индекс ассоциируемого с 
ним [bootstrap](https://stackoverflow.com/questions/30733557/what-is-a-bootstrap-method) метода.

Вот список <i>bootstrap</i> методов: 

<pre><code>
…
BootstrapMethods:
  0: #27 invokestatic java/lang/invoke/LambdaMetafactory.metafactory:(
                        Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;
                        Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodType;
                        Ljava/lang/invoke/MethodHandle;Ljava/lang/invoke/MethodType;)
                        Ljava/lang/invoke/CallSite;
    Method arguments:
      #28 (Ljava/lang/String;)V
      #29 invokestatic Java8.lambda$main$0:(Ljava/lang/String;)V
      #28 (Ljava/lang/String;)V
</code></pre>


Здесь <i>bootstrap</i> метод назван <code-inline>metafactory</code-inline> в классе <code-inline>java.lang.invoke.LambdaMetafactory</code-inline>.
Он [живет в JDK](https://docs.oracle.com/javase/8/docs/api/java/lang/invoke/LambdaMetafactory.html) и 
занимается созданием анонимных классов налету (on-the-fly) в рантайме для лямбд так же, 
как и <code-inline>D8</code-inline> генерит их в компайлтайме.

Если взглянуть на [документацию Android](https://developer.android.com/reference/java/lang/invoke/package-summary) к <code-inline>java.lang.invoke</code-inline>
или на [исходники AOSP](https://android.googlesource.com/platform/libcore/+/master/ojluni/src/main/java/java/lang/invoke/)
к <code-inline>java.lang.invoke</code-inline>, увидим, что в рантайме этого класса нет. 
Вот поэтому дешугаринг всегда происходит во время компиляции, независимо от того, какой у вас minApi. VM поддерживает
байткод инструкцию, похожую на <code-inline>invokedynamic</code-inline>, но встроенный в JDK <code-inline>LambdaMetafactory</code-inline> недоступен для использования.

## \#\# Method References

Вместе с лямбдами в Java 8 добавили ссылки на методы — это эффективный способ создать лямбду, 
тело которой ссылается на уже существующий метод.

Наш интерфейс <code-inline>Logger</code-inline> как раз является таким примером. 
Тело лямбды ссылалось на <code-inline>System.out.println</code-inline>. Давайте превратим лямбду в метод референc:

<pre><code class="diff">
public static void main(String... args) {
-    sayHi(s -> System.out.println(s));
+    sayHi(System.out::println);
   }
</code></pre>


Когда мы это скомпилируем и взглянем на байткод, то увидим одно различие с предыдущей версией: 

<pre><code>
[000268] -$$Lambda$1Osqr2Z9OSwjseX_0FMQJcCG_uM.log:(Ljava/lang/String;)V
0000: iget-object v0, v1, L-$$Lambda$1Osqr2Z9OSwjseX_0FMQJcCG_uM;.f$0:Ljava/io/PrintStream;
0002: invoke-virtual {v0, v2}, Ljava/io/PrintStream;.println:(Ljava/lang/String;)V
0005: return-void
</code></pre>


Вместо вызова сгенерированного <code-inline>Java8.lambda$main$0</code-inline>, который содержит вызов <code-inline>System.out.println</code-inline>,
теперь <code-inline>System.out.println</code-inline> вызывается напрямую.

Класс с лямбдой больше не <code-inline>static</code-inline> синглтон, а по индексу <code-inline>0000</code-inline> в байткоде видно,
что мы получаем ссылку на <code-inline>PrintStream</code-inline> — <code-inline>System.out</code-inline>, 
который затем используется для того, чтобы вызвать на нем <code-inline>println</code-inline>.

В итоге наш класс превратился в это:

<pre><code class="diff">
public static void main(String... args) {
-    sayHi(System.out::println);
+    sayHi(new -$$Lambda$1Osqr2Z9OSwjseX_0FMQJcCG_uM(System.out));
   }
@@
 }
+
+class -$$Lambda$1Osqr2Z9OSwjseX_0FMQJcCG_uM implements Java8.Logger {
+  private final PrintStream ps;
+
+  -$$Lambda$1Osqr2Z9OSwjseX_0FMQJcCG_uM(PrintStream ps) {
+    this.ps = ps;
+  }
+
+  @Override public void log(String s) {
+    ps.println(s);
+  }
+}
</code></pre>

## \#\# Default и static методы в интерфейсах

Еще одним важным и серьезным изменением, которое принесла Java 8, стала возможность объявлять <code-inline>default</code-inline>
и <code-inline>static</code-inline> методы в интерфейсах.

<pre><code>
interface Logger {
  void log(String s);

  default void log(String tag, String s) {
    log(tag + ": " + s);
  }

  static Logger systemOut() {
    return System.out::println;
  }
}
</code></pre>


Все это тоже поддерживается D8. Используя те же инструменты, что и ранее, несложно увидеть задешугаренную версию Logger’a 
с <code-inline>default</code-inline> и <code-inline>static</code-inline> методами. 
Одно из различий с лямбдами и <code-inline>method references</code-inline> в том, что дефолтные и статик методы реализованы
в Android VM и, начиная с 24 API, D8 не будет <i>дешугарить</i> их.

## \#\# Может, просто использовать Kotlin?

Читая статью, большинство из вас, наверное, подумали о Kotlin. Да, он поддерживает все фичи Java 8, но реализованы
они <code-inline>kotlinc</code-inline> точно так же, как и D8, за исключением некоторых деталей.

Поэтому поддержка Андроидом новых версий Java до сих пор очень важна, даже если ваш проект на 100% написан на Kotlin. 

Не исключено, что в будущем Kotlin перестанет поддерживать байткод Java 6 и Java 7. 
[IntelliJ IDEA](https://blog.jetbrains.com/idea/2015/12/intellij-idea-16-eap-144-2608-is-out/), Gradle 5.0 перешли на Java 8.
Количество платформ, работающих на более старых JVM, сокращается.

## \#\# Desugaring APIs

Все это время я рассказывал про фичи Java 8, но ничего не говорил о новых API — стримы, 
<code-inline>CompletableFuture</code-inline>, date/time и так далее.

Возвращаясь к примеру с Logger’ом, мы можем использовать новый API даты/времени, чтобы узнать, когда сообщения были отправлены.

<pre><code>
import java.time.*;

class Java8 {
  interface Logger {
    void log(LocalDateTime time, String s);
  }

  public static void main(String... args) {
    sayHi((time, s) -> System.out.println(time + " " + s));
  }

  private static void sayHi(Logger logger) {
    logger.log(LocalDateTime.now(), "Hello!");
  }
}
</code></pre>


Снова компилируем это с помощью <code-inline>javac</code-inline> и преобразуем его в байткод Dalvik с D8, 
который <i>дешугарит</i> его для поддержки на всех версиях API.

<pre><code>
$ javac *.java

$ java -jar d8.jar \
    --lib $ANDROID_HOME/platforms/android-28/android.jar \
    --release \
    --output . \
    *.class
</code></pre>


Можете даже запушить это на свой девайс, чтобы убедиться, что оно работает.

<pre><code>
$ adb push classes.dex /sdcard
classes.dex: 1 file pushed. 0.5 MB/s (1620 bytes in 0.003s)

$ adb shell dalvikvm -cp /sdcard/classes.dex Java8
2018-11-19T21:38:23.761 Hello
</code></pre>


Если на этом устройстве API 26 и выше, появится месседж Hello. Если нет — увидим следующее:

<pre><code>
java.lang.NoClassDefFoundError: Failed resolution of: Ljava/time/LocalDateTime;
  at Java8.sayHi(Java8.java:13)
  at Java8.main(Java8.java:9)
</code></pre>


D8 справился с лямбдами, метод референсами, но не сделал ничего для работы с <code-inline>LocalDateTime</code-inline>, и это очень печально.

Разработчикам приходится использовать свои собственные реализации или обертки над date/time api, либо использовать библиотеки
по типу <code-inline>ThreeTenBP</code-inline> для работы со временем, но почему то, что ты можешь написать руками, 
не может сделать D8?

## \#\# Эпилог
Отсутствие поддержки всех новых API Java 8 остается большой проблемой в экосистеме Android.
Ведь вряд ли каждый из нас может позволить указать 26 min API в своем проекте. Библиотеки, поддерживающие и Android и JVM, 
не могут позволить себе использовать API, представленный нам 5 лет назад! 

И даже несмотря на то, что саппорт Java 8 теперь является частью D8, каждый разработчик все равно должен явно указывать 
source и target compatibility на Java 8. Если вы пишете собственные библиотеки, то можете усилить эту тенденцию, 
выкладывая библиотеки, которые используют Java 8 байткод (даже если вы не используете новые фичи языка).

Над D8 ведется очень много работ, поэтому, кажется, в будущем с поддержкой фичей языка все будет ок. 
Даже если вы пишете только на Kotlin, очень важно заставлять команду разработки Android поддерживать все новые версии Java,
улучшать байткод и новые API. 

Этот пост — письменная версия моего выступления [Digging into D8 and R8](https://jakewharton.com/digging-into-d8-and-r8/).