// Sample data + shared icons for the Sekai Dreams UI kit.
const img = (seed) => `https://picsum.photos/seed/${seed}/640/480`;

const DREAMS = [
  { id: 1, n: 1, title: "オーロラを見る", status: "active",
    desc: "アイスランドかノルウェーで、冬の夜空を埋めるオーロラを自分の目で見る。写真ではなく、本物の光のカーテンを。",
    images: [img("aurora1"), img("aurora2"), img("aurora3"), img("aurora4")] },
  { id: 2, n: 2, title: "フルマラソンを完走する", status: "done",
    desc: "42.195kmを自分の脚で走りきる。タイムは問わない。ゴールテープを切るその瞬間を味わう。",
    images: [img("run1"), img("run2")] },
  { id: 3, n: 3, title: "本を一冊書く", status: "draft",
    desc: "いつか自分の言葉で、一冊の本を書き上げたい。テーマはまだ決まっていない。", images: [] },
  { id: 4, n: 4, title: "京都で桜を見る", status: "done",
    desc: "哲学の道を、満開の桜の下で歩く。朝のいちばん静かな時間に。",
    images: [img("sakura1"), img("sakura2"), img("sakura3")] },
  { id: 5, n: 5, title: "ピアノでノクターンを弾く", status: "active",
    desc: "ショパンのノクターン第2番を、最後まで通して弾けるようになる。",
    images: [img("piano1")] },
  { id: 6, n: 6, title: "自分のカフェを開く", status: "active",
    desc: "小さくていい。好きな珈琲と、静かな音楽と、誰かが長居したくなる席のある店を持つ。",
    images: [img("cafe1"), img("cafe2"), img("cafe3"), img("cafe4"), img("cafe5")] },
  { id: 7, n: 7, title: "両親を旅行に連れて行く", status: "draft",
    desc: "元気なうちに、温泉でもいい、ふたりをゆっくりした旅に連れて行きたい。", images: [] },
  { id: 8, n: 8, title: "星空の下でキャンプ", status: "done",
    desc: "街の灯りが届かない場所で、天の川が見えるほどの星空の下、一晩を過ごす。",
    images: [img("camp1"), img("camp2")] },
  { id: 9, n: 9, title: "海外で一年暮らす", status: "active",
    desc: "観光ではなく、生活として、ひとつの街に一年腰を据えてみたい。",
    images: [img("city1"), img("city2"), img("city3")] },
];

const TOTAL = 100;

Object.assign(window, { DREAMS, TOTAL });
