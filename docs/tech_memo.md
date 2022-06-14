# technical memo

## pythonからメソッド実行した場合の処理

pythonアプリからメソッド実行した場合、どのような流れで実行するかをカメラクラスの生成を例に説明する。カメラクラス生成以外も同じ流れで処理は行われる。

#### Pythonアプリでカメラ生成

カメラ生成Factory

https://d2ezksrziasiu7.cloudfront.net/v0/004/_build/pyjds.html#pyjds.device_factory.DeviceFactory.create

カメラ生成Factoryのcreate()メソッドでは`_module.Device.create()`を実行する。`_module`はpymoduleをbuildしたpydファイルになる。

https://github.com/jai-rd/pyJds/blob/bd46a31f23e82ecb22a88a098fbd190352ff02ce/python/src/pyjds/device_factory.py#L58

#### _module.Device

`_module.Device.create`は以下宣言してあり、これは`ModDevice::Create()`を実行する。

https://github.com/jai-rd/pyJds/blob/bd46a31f23e82ecb22a88a098fbd190352ff02ce/src/pymodule/module.cpp#L127-L128

#### ModDevice::Create()

jaids-coreの`core::Device::Create()`メソッドが実行されDeviceが生成される。std::unique_ptr<ModDevice>を返却する事でPython側でObjectがdeleteされたタイミングでModDeviceもdeleteされる。

https://github.com/jai-rd/pyJds/blob/bd46a31f23e82ecb22a88a098fbd190352ff02ce/src/libcpp/mod_device.cpp#L60-L67



## カメラからの画像取得

カメラからの画像取得は[Stream#get_buffer()](https://d2ezksrziasiu7.cloudfront.net/v0/004/_build/pyjds.html#pyjds.stream.Stream.get_buffer)を実行する事で[Buffer](https://d2ezksrziasiu7.cloudfront.net/v0/004/_build/pyjds.html#pyjds.buffer.Buffer)が取得できる。この時の状態はeBUS SDKの`PvStream#RetrieveBuffer()`を実行した時と同じ状態である。つまり`PvStream#QueueBuffer()`を実行していない状態となっている。したがって[Buffer](https://d2ezksrziasiu7.cloudfront.net/v0/004/_build/pyjds.html#pyjds.buffer.Buffer)をアプリ側で保持続けた場合、画像取得Queueに空きバッファが存在しなくなり、画像取得が停止する。

eBUS SDKでは画像取得Queueにバッファを追加するために`PvStream#QueueBuffer()`メソッドを利用するがpyjdsでは該当メソッドは存在しない。pyjdsでは[Buffer](https://d2ezksrziasiu7.cloudfront.net/v0/004/_build/pyjds.html#pyjds.buffer.Buffer)がガベージコレクションで開放されたタイミングで`PvStream#QueueBuffer()`を行なっている。  


### Buffer#get_image()
[Buffer#get_image()](https://d2ezksrziasiu7.cloudfront.net/v0/004/_build/pyjds.html#pyjds.buffer.Buffer.get_image)を実行することで[Image](https://d2ezksrziasiu7.cloudfront.net/v0/004/_build/pyjds.html#pyjds.buffer.Buffer.get_image)クラスが取得可能である。[Image](https://d2ezksrziasiu7.cloudfront.net/v0/004/_build/pyjds.html#pyjds.buffer.Buffer.get_image)はndarray型の画像データと属性値をもつ。
[Buffer#get_image()](https://d2ezksrziasiu7.cloudfront.net/v0/004/_build/pyjds.html#pyjds.buffer.Buffer.get_image)実行時、より正確には[Image](https://d2ezksrziasiu7.cloudfront.net/v0/004/_build/pyjds.html#pyjds.buffer.Buffer.get_image)クラスのコンストラクタでカメラから取得したRAW画像をndarray形式へ変換を実行している。
[Image](https://d2ezksrziasiu7.cloudfront.net/v0/004/_build/pyjds.html#pyjds.buffer.Buffer.get_image)クラスはeBUS SDKのPvBufferとは独立しておりImageクラスをUserアプリで保持する分には問題ない。

ただしImageクラスのコンストラクタで画像変換を行うため、get_image()を実行すると変換処理のコストが発生する。また上記理由からRGB8,Mono8のような変換必要ないPixelFormatであっても一定のコストが発生する。


# Buffer -> Image変換
### 変換処理時間

Python版でBufferをndarray変換処理時間(ms)

<details>
  <summary>CPU Info</summary>

![image](https://user-images.githubusercontent.com/59547254/155103556-e4eacb84-f0a2-46e8-9de5-7d4ebdfbe90a.png)
</details>

#### AP-1600T-PGE
<details>
  <summary>AP-1600T-PGE</summary>

```
2022-02-24 17:49:20,718 root run [DEBUG]: ********* w:1456 h:1088 *********
2022-02-24 17:49:20,736 root run [DEBUG]: number of stream:1
2022-02-24 17:49:20,736 root run [INFO]: *************** DebayerType.SIMPLE, thread_num=1 ***************
2022-02-24 17:49:21,070 root acquire_convert [INFO]: RGB8 3 time conversions:3.7151999999998075ms, average:1.238400ms
2022-02-24 17:49:21,438 root acquire_convert [INFO]: RGB10V1Packed 3 time conversions:10.173800000000455ms, average:3.391267ms
2022-02-24 17:49:21,814 root acquire_convert [INFO]: RGB10p32 3 time conversions:11.894999999999545ms, average:3.965000ms
2022-02-24 17:49:22,194 root acquire_convert [INFO]: RGB12V1Packed 3 time conversions:11.788600000000038ms, average:3.929533ms
2022-02-24 17:49:22,203 root run [INFO]: *************** DebayerType.SIMPLE, thread_num=4 ***************
2022-02-24 17:49:22,536 root acquire_convert [INFO]: RGB8 3 time conversions:2.771300000000032ms, average:0.923767ms
2022-02-24 17:49:22,896 root acquire_convert [INFO]: RGB10V1Packed 3 time conversions:7.582900000000059ms, average:2.527633ms
2022-02-24 17:49:23,267 root acquire_convert [INFO]: RGB10p32 3 time conversions:7.909500000000236ms, average:2.636500ms
2022-02-24 17:49:23,648 root acquire_convert [INFO]: RGB12V1Packed 3 time conversions:7.591700000000756ms, average:2.530567ms
2022-02-24 17:49:23,659 root run [INFO]: *************** DebayerType.INTERPOLATION, thread_num=1 ***************
2022-02-24 17:49:24,002 root acquire_convert [INFO]: RGB8 3 time conversions:4.588799999999615ms, average:1.529600ms
2022-02-24 17:49:24,371 root acquire_convert [INFO]: RGB10V1Packed 3 time conversions:11.63610000000137ms, average:3.878700ms
2022-02-24 17:49:24,742 root acquire_convert [INFO]: RGB10p32 3 time conversions:8.997400000000155ms, average:2.999133ms
2022-02-24 17:49:25,118 root acquire_convert [INFO]: RGB12V1Packed 3 time conversions:11.899499999999286ms, average:3.966500ms
2022-02-24 17:49:25,129 root run [INFO]: *************** DebayerType.INTERPOLATION, thread_num=4 ***************
2022-02-24 17:49:25,471 root acquire_convert [INFO]: RGB8 3 time conversions:4.147000000000567ms, average:1.382333ms
2022-02-24 17:49:25,836 root acquire_convert [INFO]: RGB10V1Packed 3 time conversions:6.524399999998209ms, average:2.174800ms
2022-02-24 17:49:26,203 root acquire_convert [INFO]: RGB10p32 3 time conversions:7.375900000000435ms, average:2.458633ms
2022-02-24 17:49:26,582 root acquire_convert [INFO]: RGB12V1Packed 3 time conversions:7.713800000000326ms, average:2.571267ms
2022-02-24 17:49:26,593 root run [INFO]: *************** DebayerType.INTERPOLATION, thread_num=8 ***************
2022-02-24 17:49:26,935 root acquire_convert [INFO]: RGB8 3 time conversions:4.584299999997654ms, average:1.528100ms
2022-02-24 17:49:27,301 root acquire_convert [INFO]: RGB10V1Packed 3 time conversions:7.799699999999632ms, average:2.599900ms
2022-02-24 17:49:27,667 root acquire_convert [INFO]: RGB10p32 3 time conversions:8.203699999999259ms, average:2.734567ms
2022-02-24 17:49:28,047 root acquire_convert [INFO]: RGB12V1Packed 3 time conversions:8.39859999999959ms, average:2.799533ms
```
</details>

#### GOX-5103M-PGE
<details>
  <summary>GOX-5103M-PGE</summary>

```
2022-02-24 17:56:44,814 root run [DEBUG]: ********* w:2448 h:2048 *********
2022-02-24 17:56:44,828 root run [DEBUG]: number of stream:1
2022-02-24 17:56:44,828 root run [INFO]: *************** DebayerType.SIMPLE, thread_num=1 ***************
2022-02-24 17:56:45,303 root acquire_convert [INFO]: Mono8 3 time conversions:3.127800000000125ms, average:1.042600ms
2022-02-24 17:56:46,173 root acquire_convert [INFO]: Mono10 3 time conversions:8.121099999999881ms, average:2.707033ms
2022-02-24 17:56:47,334 root acquire_convert [INFO]: Mono10Packed 3 time conversions:14.315900000000603ms, average:4.771967ms
2022-02-24 17:56:48,214 root acquire_convert [INFO]: Mono12 3 time conversions:10.119899999999404ms, average:3.373300ms
2022-02-24 17:56:49,381 root acquire_convert [INFO]: Mono12Packed 3 time conversions:12.601000000000084ms, average:4.200333ms
2022-02-24 17:56:49,705 root run [INFO]: *************** DebayerType.SIMPLE, thread_num=4 ***************
2022-02-24 17:56:50,206 root acquire_convert [INFO]: Mono8 3 time conversions:3.523599999999405ms, average:1.174533ms
2022-02-24 17:56:51,090 root acquire_convert [INFO]: Mono10 3 time conversions:7.1672000000013725ms, average:2.389067ms
2022-02-24 17:56:51,953 root acquire_convert [INFO]: Mono10Packed 3 time conversions:8.658700000001573ms, average:2.886233ms
2022-02-24 17:56:53,150 root acquire_convert [INFO]: Mono12 3 time conversions:8.089399999999358ms, average:2.696467ms
2022-02-24 17:56:54,017 root acquire_convert [INFO]: Mono12Packed 3 time conversions:7.857400000002457ms, average:2.619133ms
2022-02-24 17:56:54,662 root run [INFO]: *************** DebayerType.SIMPLE, thread_num=8 ***************
2022-02-24 17:56:55,162 root acquire_convert [INFO]: Mono8 3 time conversions:3.262199999999993ms, average:1.087400ms
2022-02-24 17:56:56,043 root acquire_convert [INFO]: Mono10 3 time conversions:7.905199999999724ms, average:2.635067ms
2022-02-24 17:56:56,903 root acquire_convert [INFO]: Mono10Packed 3 time conversions:8.433400000001257ms, average:2.811133ms
2022-02-24 17:56:57,790 root acquire_convert [INFO]: Mono12 3 time conversions:7.698699999998837ms, average:2.566233ms
2022-02-24 17:56:58,649 root acquire_convert [INFO]: Mono12Packed 3 time conversions:8.531900000001258ms, average:2.843967ms
2022-02-24 17:56:58,972 root run [INFO]: *************** DebayerType.INTERPOLATION, thread_num=1 ***************
2022-02-24 17:56:59,473 root acquire_convert [INFO]: Mono8 3 time conversions:3.414200000001699ms, average:1.138067ms
2022-02-24 17:57:00,357 root acquire_convert [INFO]: Mono10 3 time conversions:10.448800000006031ms, average:3.482933ms
2022-02-24 17:57:01,217 root acquire_convert [INFO]: Mono10Packed 3 time conversions:14.159199999998151ms, average:4.719733ms
2022-02-24 17:57:02,107 root acquire_convert [INFO]: Mono12 3 time conversions:9.958999999998497ms, average:3.319667ms
2022-02-24 17:57:02,967 root acquire_convert [INFO]: Mono12Packed 3 time conversions:14.280399999996973ms, average:4.760133ms
2022-02-24 17:57:03,293 root run [INFO]: *************** DebayerType.INTERPOLATION, thread_num=4 ***************
2022-02-24 17:57:03,802 root acquire_convert [INFO]: Mono8 3 time conversions:3.9457000000027165ms, average:1.315233ms
2022-02-24 17:57:04,677 root acquire_convert [INFO]: Mono10 3 time conversions:7.771200000000533ms, average:2.590400ms
2022-02-24 17:57:05,542 root acquire_convert [INFO]: Mono10Packed 3 time conversions:7.121599999997841ms, average:2.373867ms
2022-02-24 17:57:06,421 root acquire_convert [INFO]: Mono12 3 time conversions:8.175799999996514ms, average:2.725267ms
2022-02-24 17:57:07,287 root acquire_convert [INFO]: Mono12Packed 3 time conversions:6.882499999996128ms, average:2.294167ms
2022-02-24 17:57:07,933 root run [INFO]: *************** DebayerType.INTERPOLATION, thread_num=8 ***************
2022-02-24 17:57:08,433 root acquire_convert [INFO]: Mono8 3 time conversions:3.4479999999987854ms, average:1.149333ms
2022-02-24 17:57:09,305 root acquire_convert [INFO]: Mono10 3 time conversions:7.892499999996971ms, average:2.630833ms
2022-02-24 17:57:10,459 root acquire_convert [INFO]: Mono10Packed 3 time conversions:8.276700000003245ms, average:2.758900ms
2022-02-24 17:57:11,352 root acquire_convert [INFO]: Mono12 3 time conversions:8.395699999997674ms, average:2.798567ms
2022-02-24 17:57:12,209 root acquire_convert [INFO]: Mono12Packed 3 time conversions:8.151000000001574ms, average:2.717000ms
```
</details>

#### GOX-5103C-PGE
<details>
  <summary>GOX-5103C-PGE</summary>

```
2022-02-24 18:00:00,564 root run [DEBUG]: ********* w:2448 h:2048 *********
2022-02-24 18:00:00,578 root run [DEBUG]: number of stream:1
2022-02-24 18:00:00,578 root run [INFO]: *************** DebayerType.SIMPLE, thread_num=1 ***************
2022-02-24 18:00:00,902 root acquire_convert [INFO]: BayerRG8 3 time conversions:22.52110000000007ms, average:7.507033ms
2022-02-24 18:00:01,644 root acquire_convert [INFO]: BayerRG10 3 time conversions:45.522199999999735ms, average:15.174067ms
2022-02-24 18:00:02,411 root acquire_convert [INFO]: BayerRG10Packed 3 time conversions:46.435600000000576ms, average:15.478533ms
2022-02-24 18:00:03,160 root acquire_convert [INFO]: BayerRG12 3 time conversions:41.18729999999893ms, average:13.729100ms
2022-02-24 18:00:03,925 root acquire_convert [INFO]: BayerRG12Packed 3 time conversions:47.76060000000015ms, average:15.920200ms
2022-02-24 18:00:04,252 root run [INFO]: *************** DebayerType.SIMPLE, thread_num=4 ***************
2022-02-24 18:00:04,608 root acquire_convert [INFO]: BayerRG8 3 time conversions:11.955100000000662ms, average:3.985033ms
2022-02-24 18:00:05,342 root acquire_convert [INFO]: BayerRG10 3 time conversions:20.06439999999987ms, average:6.688133ms
2022-02-24 18:00:06,062 root acquire_convert [INFO]: BayerRG10Packed 3 time conversions:26.43799999999974ms, average:8.812667ms
2022-02-24 18:00:06,805 root acquire_convert [INFO]: BayerRG12 3 time conversions:20.119099999998724ms, average:6.706367ms
2022-02-24 18:00:07,518 root acquire_convert [INFO]: BayerRG12Packed 3 time conversions:26.338299999999037ms, average:8.779433ms
2022-02-24 18:00:07,846 root run [INFO]: *************** DebayerType.SIMPLE, thread_num=8 ***************
2022-02-24 18:00:08,204 root acquire_convert [INFO]: BayerRG8 3 time conversions:11.636199999999874ms, average:3.878733ms
2022-02-24 18:00:08,925 root acquire_convert [INFO]: BayerRG10 3 time conversions:16.320200000000895ms, average:5.440067ms
2022-02-24 18:00:09,644 root acquire_convert [INFO]: BayerRG10Packed 3 time conversions:24.69950000000054ms, average:8.233167ms
2022-02-24 18:00:10,368 root acquire_convert [INFO]: BayerRG12 3 time conversions:15.772699999999418ms, average:5.257567ms
2022-02-24 18:00:11,085 root acquire_convert [INFO]: BayerRG12Packed 3 time conversions:24.18939999999914ms, average:8.063133ms
2022-02-24 18:00:11,413 root run [INFO]: *************** DebayerType.INTERPOLATION, thread_num=1 ***************
2022-02-24 18:00:11,765 root acquire_convert [INFO]: BayerRG8 3 time conversions:22.506200000000476ms, average:7.502067ms
2022-02-24 18:00:12,500 root acquire_convert [INFO]: BayerRG10 3 time conversions:41.004600000000835ms, average:13.668200ms
2022-02-24 18:00:13,261 root acquire_convert [INFO]: BayerRG10Packed 3 time conversions:54.323199999998906ms, average:18.107733ms
2022-02-24 18:00:14,011 root acquire_convert [INFO]: BayerRG12 3 time conversions:40.78499999999785ms, average:13.595000ms
2022-02-24 18:00:14,777 root acquire_convert [INFO]: BayerRG12Packed 3 time conversions:55.0904999999986ms, average:18.363500ms
2022-02-24 18:00:15,104 root run [INFO]: *************** DebayerType.INTERPOLATION, thread_num=4 ***************
2022-02-24 18:00:15,461 root acquire_convert [INFO]: BayerRG8 3 time conversions:12.454899999998048ms, average:4.151633ms
2022-02-24 18:00:16,199 root acquire_convert [INFO]: BayerRG10 3 time conversions:17.897000000001384ms, average:5.965667ms
2022-02-24 18:00:16,914 root acquire_convert [INFO]: BayerRG10Packed 3 time conversions:25.778099999996584ms, average:8.592700ms
2022-02-24 18:00:17,654 root acquire_convert [INFO]: BayerRG12 3 time conversions:18.081099999996297ms, average:6.027033ms
2022-02-24 18:00:18,374 root acquire_convert [INFO]: BayerRG12Packed 3 time conversions:26.629599999999698ms, average:8.876533ms
2022-02-24 18:00:18,700 root run [INFO]: *************** DebayerType.INTERPOLATION, thread_num=8 ***************
2022-02-24 18:00:19,057 root acquire_convert [INFO]: BayerRG8 3 time conversions:11.112600000000583ms, average:3.704200ms
2022-02-24 18:00:19,786 root acquire_convert [INFO]: BayerRG10 3 time conversions:18.583199999998357ms, average:6.194400ms
2022-02-24 18:00:20,512 root acquire_convert [INFO]: BayerRG10Packed 3 time conversions:22.833800000000792ms, average:7.611267ms
2022-02-24 18:00:21,252 root acquire_convert [INFO]: BayerRG12 3 time conversions:18.662899999998928ms, average:6.220967ms
2022-02-24 18:00:21,970 root acquire_convert [INFO]: BayerRG12Packed 3 time conversions:22.531799999999436ms, average:7.510600ms
```
</details>

