/*jshint esversion: 8 */
/*jshint strict: false */


const set_last_update = () => {
  $(".update .stats").html(vaccini.last_updated);
};

const load_italy = () => {
  vaccini.territori.forEach((t, i) => {
    if (t.nome_territorio == "Italia") {
      $(".italia #vaccinati").text(t.totale_vaccinati);
      $(".italia #deltavaccinati").text(t.nuovi_vaccinati);
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
    let nome_territorio;
    if (t.nome_territorio != "Italia") {
      if (t.codice_territorio == 06) {
        nome_territorio = "E. R.";
      } else if (t.codice_territorio == 07) {
        nome_territorio = "F. V. G.";
      } else {
        nome_territorio = t.nome_territorio;
      }

      let new_tr = `<tr id="${t.codice_territorio}" class="territorio">`;
      new_tr += `<td>${nome_territorio}</td>`;
      new_tr += `<td>${t.totale_vaccinati} (+${t.nuovi_vaccinati})</td>`;
      new_tr += `<td>${t.totale_dosi_consegnate}  (+${t.nuove_dosi_consegnate})</td>`;
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
