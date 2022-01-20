
document.querySelector("#bankPaymentBtn").addEventListener('click', showBankPaymentModal)
document.querySelector('.modalClose').addEventListener('click', closePayemntModal)
document.querySelector("#cryptoPaymentBtn").addEventListener('click', showCryptoPaymentModal)

function showBankPaymentModal(e){
    e.preventDefault()
    document.querySelector('#modalBankPayment').style.display = "block"
}

function showCryptoPaymentModal(e){
    e.preventDefault()
    document.querySelector('#modalCryptoPayment').style.display = "block"
}

function closePayemntModal(){
    document.querySelector('.payment_modal__payment').style.display = "none"
}

// QRCode generator
let  qrCode = new QRCode("qrcode", {
    width: 220,
    height: 200,
    colorDark: "#000000", // foreground color
    colorLight: "#ffffff", // background-color
    correctLevel: QRCode.CorrectLevel.H,
})

new ClipboardJS(".copyTextBtn")
