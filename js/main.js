// Made by Lorenzo Rossi
// https://www.lorenzoros.si - https://github.com/lorossi

/*jshint esversion: 8 */
/*jshint strict: false */

// update the data about the last update
const set_last_update = () => {
  $(".update .stats").html(vaccini.last_updated);
};


// load the table data about Italy as a whole
const load_italy = () => {
  vaccini.territori.forEach((t, i) => {
    if (t.nome_territorio === "Italia") {
      let nuovi_vaccinati;
      if (t.nuovi_vaccinati === undefined) {
        nuovi_vaccinati = 0;
      } else {
        nuovi_vaccinati = t.nuovi_vaccinati;
      }

      let nuove_dosi;
      if (t.nuove_dosi_consegnate === undefined) {
        nuove_dosi = 0;
      } else {
        nuove_dosi = t.nuove_dosi_consegnate;
      }

      $(".italia #vaccinati").text(t.totale_vaccinati);
      $(".italia #deltavaccinati").text(nuovi_vaccinati);
      $(".italia #percentualevaccinati").text(`${t.percentuale_popolazione_vaccinata.toFixed(2)}%`);
      $(".italia #dosi").text(t.totale_dosi_consegnate);
      $(".italia #deltadosi").text(nuove_dosi);

      return;
    }
  });
};


// load data about each territory
const load_territories = (order, reverse) => {
  if (order === 0) {
    vaccini.territori.sort((a, b) => a.nome_territorio > b.nome_territorio ? 1 : -1);
  } else if (order === 1) {
    vaccini.territori.sort((a, b) => a.totale_vaccinati > b.totale_vaccinati ? 1 : -1);
  } else if (order === 2) {
    vaccini.territori.sort((a, b) => a.totale_dosi_consegnate > b.totale_dosi_consegnate ? 1 : -1);
  } else if (order === 3) {
    vaccini.territori.sort((a, b) => a.percentuale_popolazione_vaccinata > b.percentuale_popolazione_vaccinata ? 1 : -1);
  }

  if (reverse) {
    vaccini.territori.reverse();
  }

  $("table.territori tbody").html("");

  vaccini.territori.forEach((t, i) => {
    if (t.nome_territorio != "Italia") {
      let nuovi_vaccinati;
      if (t.nuovi_vaccinati === undefined) {
        nuovi_vaccinati = 0;
      } else {
        nuovi_vaccinati = t.nuovi_vaccinati;
      }

      let nuove_dosi;
      if (t.nuove_dosi === undefined) {
        nuove_dosi = 0;
      } else {
        nuove_dosi = t.nuove_dosi;
      }

      let percentuale;
      percentuale = `${parseFloat(t.percentuale_popolazione_vaccinata).toFixed(2)}%`;

      let new_tr = `<tr id="${t.codice_territorio}" class="territorio">`;
      new_tr += `<td>${t.nome_territorio}</td>`;
      new_tr += `<td>${t.totale_vaccinati} (+${nuovi_vaccinati})</td>`;
      new_tr += `<td>${t.totale_dosi_consegnate}  (+${nuove_dosi})</td>`;
      new_tr += `<td>${percentuale}</td>`;
      new_tr += "</tr>";
      $("table.territori tbody").append(new_tr);
    }
  });
};


// load data about each category
const load_categories = (order, reverse) => {
  if (order === 0) {
    vaccini.categorie.sort((a, b) => a.nome_categoria > b.nome_categoria ? 1 : -1);
  } else if (order === 1) {
    vaccini.categorie.sort((a, b) => a.totale_vaccinati > b.totale_vaccinati ? 1 : -1);
  }

  if (reverse) {
    vaccini.categorie.reverse();
  }

  $("table.categorie tbody").html("");

  vaccini.categorie.forEach((t, i) => {
    let nuovi_vaccinati;
    if (t.nuovi_vaccinati === undefined) {
      nuovi_vaccinati = 0;
    } else {
      nuovi_vaccinati = t.nuovi_vaccinati;
    }

    let new_tr = `<tr id="${t.id_categoria}" class="categorie">`;
    new_tr += `<td>${t.nome_categoria}</td>`;
    new_tr += `<td>${t.totale_vaccinati} (+${nuovi_vaccinati})</td>`;
    new_tr += "</tr>";
    $("table.categorie tbody").append(new_tr);
  });
};


// load data about each gender
const load_genders = (order, reverse) => {
  if (order === 0) {
    vaccini.sesso.sort((a, b) => a.nome_categoria > b.nome_categoria ? 1 : -1);
  } else if (order === 1) {
    vaccini.sesso.sort((a, b) => a.totale_vaccinati > b.totale_vaccinati ? 1 : -1);
  }

  if (reverse) {
    vaccini.sesso.reverse();
  }

  $("table.sesso tbody").html("");

  vaccini.sesso.forEach((t, i) => {
    let nuovi_vaccinati;
    if (t.nuovi_vaccinati === undefined) {
      nuovi_vaccinati = 0;
    } else {
      nuovi_vaccinati = t.nuovi_vaccinati;
    }

    let new_tr = `<tr id="${t.nome_categoria}" class="sesso">`;
    new_tr += `<td>${t.nome_categoria}</td>`;
    new_tr += `<td>${t.totale_vaccinati} (+${nuovi_vaccinati})</td>`;
    new_tr += "</tr>";
    $("table.sesso tbody").append(new_tr);
  });
};


// load data about age ranges
const load_age_ranges = (order, reverse) => {
  if (order === 0) {
    vaccini.fasce_eta.sort((a, b) => a.nome_categoria > b.nome_categoria ? 1 : -1);
  } else if (order === 1) {
    vaccini.fasce_eta.sort((a, b) => a.totale_vaccinati > b.totale_vaccinati ? 1 : -1);
  }

  if (reverse) {
    vaccini.fasce_eta.reverse();
  }

  $("table.fasce_eta tbody").html("");

  vaccini.fasce_eta.forEach((t, i) => {
    let nuovi_vaccinati;
    if (t.nuovi_vaccinati == undefined) {
      nuovi_vaccinati = 0;
    } else {
      nuovi_vaccinati = t.nuovi_vaccinati;
    }

    let new_tr = `<tr id="${t.nome_categoria}" class="territorio">`;
    new_tr += `<td>${t.nome_categoria}</td>`;
    new_tr += `<td>${t.totale_vaccinati} (+${nuovi_vaccinati})</td>`;
    new_tr += "</tr>";
    $("table.fasce_eta tbody").append(new_tr);
  });
};


// main function
$(document).ready(() => {
  set_last_update();
  load_italy();
  load_territories(0, false);
  load_categories(0, false);
  load_genders(0, false);
  load_age_ranges(0, false);

  // this function won't work with lambda
  $("table th").click(function() {
    let column = $(this).data("column");
    let reverse;

    if ($(this).hasClass("darr")) {
      reverse = true;
      $(this).removeClass("darr");
      $(this).addClass("uarr");
    } else {
      reverse = false;
      $(this).removeClass("uarr");
      $(this).addClass("darr");
    }

    // this is the class of the table we clicked on
    let table_class = $(this).parent().parent().parent().attr("class");
    // once we know the class, we can update its data
    if (table_class === "territori") {
      load_territories(column, reverse);
    } else if (table_class === "categorie") {
      load_categories(column, reverse);
    } else if (table_class === "sesso") {
      load_genders(column, reverse);
    } else if (table_class === "fasce_eta") {
      load_age_ranges(column, reverse);
    }

  });
});
