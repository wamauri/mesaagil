import { initImageCropScript } from "./imageCrop.js"

document.addEventListener("htmx:xhr:loadend", function(e) {
  if(e.detail.elt.innerText === "Produtos"){
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

  if($(e.detail.elt).find("h1")[0].innerText == "Categorias"){
    $("label[for=id_parent], #id_parent").attr("style", "display: none;")
  }

});
