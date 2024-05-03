"use strict";

for (let form of document.querySelectorAll(".needs-validation")) {
	console.log(form);
	form.addEventListener(
    	"submit",
    	(event) => {
			if (!event.target.checkValidity()) {
				event.preventDefault();
				event.stopPropagation();
			}
			event.target.classList.add("was-validated");
		}
  	);
}

