---
title: "httpswww.lambdanote.comproductsopendatastructures "
date: 2022-09-04T18:03:06+09:00
draft: false
---

https://www.lambdanote.com/products/opendatastructures 
もはや実装することはないと思うけど
それぞれのデータ構造の強みと弱みを知って適切に選択する必要はあるので一読の価値あり

昔メモリ上のデータを書き換えることしか概念ない時は
マージソートが何かわからなかったのが
Immutable にデータ操作するようになって
データを整列するんではなくて、分割操作で整列する
と見え方が変わったらマージソートはとても直観的だった

ヒープソートも、ソートの説明の前に
ヒープ構造で最小値を順番に取り出すのが
独立して説明してあるので、そこを乗り越えると簡単

2-4木 から 赤黒木
よくあるユースケースは 圧倒的に追加＞削除 だから
こうなったんだな
[https://www.lambdanote.com/products/opendatastructures](https://www.lambdanote.com/products/opendatastructures)
