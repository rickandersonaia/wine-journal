// This has been superceeded with a custom filter - it is retained here for
// reference

function setStars() {
    var stars = [
        '<i class="material-icons">thumb_down</i>',
        '<i class="material-icons">star_half</i>',
        '<i class="material-icons">star</i>',
        '<i class="material-icons">star</i><i class="material-icons">star_half</i>',
        '<i class="material-icons">star</i><i class="material-icons">star</i>',
        '<i class="material-icons">star</i><i class="material-icons">star</i><i class="material-icons">star_half</i>',
        '<i class="material-icons">star</i><i class="material-icons">star</i><i class="material-icons">star</i>',
        '<i class="material-icons">star</i><i class="material-icons">star</i><i class="material-icons">star</i><i class="material-icons">star_half</i>',
        '<i class="material-icons">star</i><i class="material-icons">star</i><i class="material-icons">star</i><i class="material-icons">star</i>',
        '<i class="material-icons">star</i><i class="material-icons">star</i><i class="material-icons">star</i><i class="material-icons">star</i><i class="material-icons">star_half</i>',
        '<i class="material-icons">star</i><i class="material-icons">star</i><i class="material-icons">star</i><i class="material-icons">star</i><i class="material-icons">star</i>'];

    var ratingFields = document.getElementsByClassName('star-rating');

    for (var i = 0; i < ratingFields.length; i++) {
        var rating = parseInt(ratingFields[i].innerText);
        console.log(rating)
        ratingFields[i].innerText = '';
        ratingFields[i].innerHTML = stars[rating] + ' (' + rating + ')';
    }
}