import { initImageCropScript } from "./imageCrop.js"

document.addEventListener("htmx:xhr:loadend", function(e) {
  if(e.detail.elt.innerText.includes("Produtos")){
    $("#id_price").off("focus").on("focus", function() {
      $(this).mask("#.##0,00", {reverse: true});
    });
  }
});

document.addEventListener("htmx:afterSwap", function(e) {
  const element = Array.from(e.detail.elt.children)
  .filter(elt => elt.innerText === "Adicionar Imagem")
  
  if(element.length > 0){
    initImageCropScript();
  }

  if($(e.detail.elt).find("h1")[0]){
    if($(e.detail.elt).find("h1")[0].innerText == "Categorias"){
      $("label[for=id_parent], #id_parent").attr("style", "display: none;")
    }
  }

});

$(document).on("htmx:beforeSwap", function(e) {
  if($("#productDetailModal")[0]){
    $("#productDetail")[0].children[0].remove()
  }
});

$(document).on("htmx:afterSwap", function(e) {
  const calculatePriceWithProductQuantity = (price, unitPrice, operation) => {
    if(operation === "minus"){
      return (Number(price) - Number(unitPrice))
    }
    return (Number(price) + Number(unitPrice))
  }

  const brlCurrency = (price) => {
    let reais = new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
    });
    return reais.format(price)
  }

  const convertPriceToNumber = (price) => {
    if(price.length > 6){
      return price.replace(".", "").replace(",", ".")
    }
    return price.replace(".", ",").replace(",", ".")
  }

  const changeProductPrice = (operation) => {
    let numberPrice
    let oldPrice = $("#productPrice")[0].innerText.slice(3)
    
    if(!oldPrice.includes(",")){
      oldPrice = `${oldPrice},00`
    }

    oldPrice = convertPriceToNumber(oldPrice)

    if(!localStorage.getItem("unitPrice")){
      localStorage.setItem("unitPrice", oldPrice)
    }

    let price = oldPrice
    let unitPrice = localStorage.getItem("unitPrice")
    numberPrice = calculatePriceWithProductQuantity(price, unitPrice, operation)

    $("#productPrice")[0].innerText = brlCurrency(numberPrice)
  }

  const productQuantity = () => {
    localStorage.removeItem("unitPrice")

    $("#minus").on("click", e => {
      if($("#productQuantity").get(0).innerText > 1){
        $("#productQuantity").get(0).innerText--;
        changeProductPrice("minus")
      }
    });

    $("#plus").on("click", e => {
      $("#productQuantity").get(0).innerText++;
      changeProductPrice("plus")
    });
  }

  if($("#productDetailModal")[0]){
    productQuantity();
    $("#productDetailModal").modal('show')
  }
});