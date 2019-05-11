'use strict';

// https://webrtc.ecl.ntt.com/js-tutorial.html

let localStream = null;
let peer = null;
let existingCall = null;

// ブラウザの機能を利用してデバイスのビデオおよび音声を取得する
// https://developer.mozilla.org/ja/docs/Web/API/Media_Streams_API
navigator.mediaDevices.getUserMedia({video: true, audio: true})
.then(function (stream) {
    // Success
    $('#my-video').get(0).srcObject = stream;
    localStream = stream;
}).catch(function (error) {
    // Error
    console.error('mediaDevice.getUserMedia() error:', error);
    return;
});

// P2P接続およびルーム接続機能を操作するためのクラス
// https://webrtc.ecl.ntt.com/skyway-js-sdk-doc/ja/peer/#Peer
peer = new Peer({
    key: 'apikey',
    debug: 3
});

/* 
SkyWayのシグナリングサーバと接続し、利用する準備が整ったら発火します。 SkyWayのすべての処理はこのイベント発火後に利用できるようになります。
PeerIDと呼ばれるクライアント識別用のIDがシグナリングサーバで発行され、コールバックイベントで取得できます。 PeerIDはクライアントサイドで指定することもできます。
*/
peer.on('open', function(){
    $('#my-id').text(peer.id);
});

// 何らかのエラーが発生した場合に発火
peer.on('error', function(err){
    alert(err.message);
});

// Peer（相手）との接続が切れた際に発火
peer.on('close', function(){
});

// シグナリングサーバとの接続が切れた際に発火
peer.on('disconnected', function(){
});

/*
発信処理
発信ボタンをクリックした場合に相手に発信します。
peer.call()で相手のPeerID、自分自身のlocalStreamを引数にセットし発信します。 接続するための相手のPeerIDは、別途何らかの方法で入手する必要があります。
発信後はCallオブジェクトが返ってくるため、必要なイベントリスナーをセットします。
*/
$('#make-call').submit(function(e){
    e.preventDefault();
    const call = peer.call($('#callto-id').val(), localStream);
    setupCallEventHandlers(call);
});

/*
切断処理
切断ボタンをクリックした場合に、相手との接続を切断します。 
call.close()で該当する接続を切断します。発信処理で生成したCallオブジェクトはexistingCallとして保持しておきます。 オブジェクト保持は発信処理のsetupCallEventHandlers()の中で実行
*/
$('#end-call').click(function(){
    existingCall.close();
});

/*
着信処理
相手から接続要求がきた場合に応答します。 
相手から接続要求が来た場合はcallが発火します。 引数として相手との接続を管理するためのCallオブジェクトが取得できるため、call.answer()を実行し接続要求に応答します。
この時に、自分自身のlocalStreamをセットすると、相手にカメラ映像・マイク音声を送信することができるようになります。
発信時の処理と同じくsetupCallEventHandlersを実行し、 Callオブジェクトのイベントリスナーをセットします。
*/
peer.on('call', function(call){
    call.answer(localStream);
    setupCallEventHandlers(call);
});

function setupCallEventHandlers(call){
    /*
    今回作るアプリでは既に接続中の場合は一旦既存の接続を切断し、後からきた接続要求を優先します。 
    また、切断処理等で利用するため、CallオブジェクトをexistingCallとして保持しておきます。
    */
    if (existingCall) {
        existingCall.close();
    };
    existingCall = call;
    
    // 相手のカメラ映像・マイク音声を受信した際に発火します。
    // 取得したStreamオブジェクトをvideo要素にセットします。
    call.on('stream', function(stream){
        addVideo(call,stream);
        setupEndCallUI();
        $('#their-id').text(call.remoteId);
    });

    // call.close()による切断処理が実行され、実際に切断されたら発火します。 
    // このイベントは、call.close()実行した側、実行された側それぞれで発火します。call.peerで切断した相手のPeerIDを取得できます。
    call.on('close', function(){
        removeVideo(call.remoteId);
        setupMakeCallUI();
    });
}

/* UIセットアップ */
// video要素の再生
function addVideo(call,stream){
    $('#their-video').get(0).srcObject = stream;
}

// video要素の削除
function removeVideo(peerId){
    $('#their-video').get(0).srcObject = undefined;
}

// ボタンの表示、非表示切り替え
function setupMakeCallUI(){
    $('#make-call').show();
    $('#end-call').hide();
}

function setupEndCallUI() {
    $('#make-call').hide();
    $('#end-call').show();
}