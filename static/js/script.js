let phoneOtherEl = document.querySelector(".phone-others-el")

let newsSectionPhoneOtherSection = document.querySelector(".other-sectors")

let otherSectorPlaceholder = newsSectionPhoneOtherSection.innerHTML

newsSectionPhoneOtherSection.innerHTML = ""

phoneOtherEl.addEventListener('click', function() {
    newsSectionPhoneOtherSection.innerHTML = `<div class="other-sectors"> ${otherSectorPlaceholder} </div>`
});

document.body.addEventListener("click", function (event) {
    if (event.target.closest(".close-others")) {
        newsSectionPhoneOtherSection.innerHTML = "";
    }
});