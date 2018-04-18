// Inspired by Chris Coyier's Range Input Value Bubbles
//     https://codepen.io/chriscoyier/pen/imdrE

function modifyOffset() {
	var el, newPoint, newPlace, offset, siblings, k;
	var dsa = ['0', '$', '$$', '$$$', '$$$$', '5$']
	width    = this.offsetWidth;
	newPoint = (this.value - this.getAttribute("min")) / (this.getAttribute("max") - this.getAttribute("min"));
	offset   = 0.5;
	if (newPoint < 0) { newPlace = 0;  }
	else if (newPoint > 1) { newPlace = width; }
	else { newPlace = width * newPoint + offset; offset -= newPoint;}
	siblings = this.parentNode.childNodes;
	for (var i = 0; i < siblings.length; i++) {
		sibling = siblings[i];
		if (sibling.id == this.id) { k = true; }
		if ((k == true) && (sibling.nodeName == "OUTPUT")) {
			outputTag = sibling;
		}
	}
	console.log(this.value)
	outputTag.style.left       = newPlace + "px";
	outputTag.style.marginLeft = offset + "%";
	outputTag.innerHTML        = dsa[this.value];
}

function modifyInputs() {

	var input = document.getElementById("price");

	if (input.getAttribute("type") == "range") {
		input.onchange = modifyOffset;

		// the following taken from http://stackoverflow.com/questions/2856513/trigger-onchange-event-manually
		if ("fireEvent" in input) {
			input.fireEvent("onchange");
		} else {
			var evt = document.createEvent("HTMLEvents");
			evt.initEvent("change", false, true);
			input.dispatchEvent(evt);
		}
	}

}

modifyInputs();