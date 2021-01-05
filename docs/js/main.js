/*jshint esversion: 8 */
/*jshint strict: false */


const set_last_update = () => {
  $(".update .stats").html(vaccini.last_updated);
};

const load_italy = () => {
  vaccini.territori.forEach((t, i) => {
    if (t.nome_territorio == "Italia") {
      $(".italia #vaccinati").text(t.totale_vaccinati);

      let nuovi_vaccinati;
      if (t.nuovi_vaccinati == undefined) {
        nuovi_vaccinati = 0;
      } else {
        nuovi_vaccinati = t.nuovi_vaccinati;
      }

      $(".italia #deltavaccinati").text(nuovi_vaccinati);
      $(".italia #percentualevaccinati").text(`${t.percentuale_popolazione_vaccinata.toFixed(2)}%`);
      return;
    }
  });
};


const load_table = (order, reverse) => {
  if (order === 0) {
    vaccini.territori.sort((a, b) => a.nome_territorio > b.nome_territorio ? 1 : -1);
  } else if (order === 1) {
    vaccini.territori.sort((a, b) => a.totale_vaccinati > b.totale_vaccinati ? 1 : -1);
  } else if (order === 2) {
    vaccini.territori.sort((a, b) => a.totale_dosi_consegnate > b.totale_dosi_consegnate ? 1 : -1);
  }

  if (reverse) {
    vaccini.territori.reverse();
  }

  $(".territori tbody").html("");

  vaccini.territori.forEach((t, i) => {
    if (t.nome_territorio != "Italia") {
      let nuovi_vaccinati;
      if (t.nuovi_vaccinati == undefined) {
        nuovi_vaccinati = 0;
      } else {
        nuovi_vaccinati = t.nuovi_vaccinati;
      }
      let nuove_dosi;
      if (t.nuove_dosi == undefined) {
        nuove_dosi = 0;
      } else {
        nuove_dosi = t.nuove_dosi;
      }

      let new_tr = `<tr id="${t.codice_territorio}" class="territorio">`;
      new_tr += `<td>${t.nome_territorio}</td>`;
      new_tr += `<td>${t.totale_vaccinati} (+${nuovi_vaccinati})</td>`;
      new_tr += `<td>${t.totale_dosi_consegnate}  (+${nuove_dosi})</td>`;
      new_tr += "</tr>";
      $(".territori tbody").append(new_tr);
    }
  });
};

$(document).ready(() => {
  set_last_update();
  load_italy();
  load_table(0, false);

  $("table.territori th").click(function() {
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

    load_table(column, reverse);
  });
});
