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

      $(".italia #vaccinati").text(`${t.totale_vaccinati}`);
      $(".italia #deltavaccinati").text(`${nuovi_vaccinati}`);
      $(".italia #dosi").text(`${t.totale_dosi_consegnate}`);
      $(".italia #deltadosi").text(`${nuove_dosi}`);
      $(".italia #percentualevaccinati").text(`${t.percentuale_popolazione_vaccinata.toFixed(2)}%`);
      $(".italia #percentualenecessaria").text(`60-80%`);

      return;
    }
  });
};


// load data about each territory
const load_territories = (order, reverse) => {
  // sort data
  if (order === 0) {
    vaccini.territori.sort((a, b) => a.nome_territorio > b.nome_territorio ? 1 : -1);
  } else if (order === 1) {
    vaccini.territori.sort((a, b) => a.totale_vaccinati > b.totale_vaccinati ? 1 : -1);
  } else if (order === 2) {
    vaccini.territori.sort((a, b) => a.percentuale_popolazione_vaccinata > b.percentuale_popolazione_vaccinata ? 1 : -1);
  } else if (order === 3) {
    vaccini.territori.sort((a, b) => a.totale_dosi_consegnate > b.totale_dosi_consegnate ? 1 : -1);
  }

  if (reverse) {
    vaccini.territori.reverse();
  }

  // fill table
  $("table#territori tbody").html("");

  vaccini.territori.forEach((t, i) => {
    if (t.nome_territorio != "Italia") {
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

      let percentuale;
      percentuale = `${parseFloat(t.percentuale_popolazione_vaccinata).toFixed(2)}%`;

      let new_tr = `<tr id="${t.codice_territorio}" class="territorio">`;
      new_tr += `<td>${t.nome_territorio}</td>`;
      new_tr += `<td>${t.totale_vaccinati} (+${nuovi_vaccinati})</td>`;
      new_tr += `<td>${percentuale}</td>`;
      new_tr += `<td>${t.totale_dosi_consegnate}  (+${nuove_dosi})</td>`;
      new_tr += "</tr>";
      $("table#territori tbody").append(new_tr);
    }
  });
};

const load_territories_chart = (order, sort_by_name, old_chart) => {
  // chart variables
  let chart;
  let data;
  let label;
  let labels;
  let background_colors;
  let border_colors;
  let hover_background_colors;
  let font_size;

  // sort data and fill variables
  if (order === 0) {
    vaccini.territori.sort((a, b) => a.totale_vaccinati > b.totale_vaccinati ? 1 : -1);
    if (sort_by_name == true) {
      vaccini.territori.sort((a, b) => a.nome_territorio > b.nome_territorio ? 1 : -1);
    }
    data = vaccini.territori.filter(x => x.nome_territorio != "Italia").map(x => x.totale_vaccinati);
    background_colors = data.map(x => `hsla(${x / Math.max(...data) * 120}, 100%, 50%, 0.5)`);
    border_colors = data.map(x => `hsl(${x / Math.max(...data) * 120}, 100%, 50%)`);
    hover_background_colors = data.map(x => `hsla(${x / Math.max(...data) * 120}, 100%, 50%, 0.25)`);
    labels = vaccini.territori.filter(x => x.nome_territorio != "Italia").map(x => x.nome_territorio);
    label = "Totale vaccinati";
  } else if (order === 1) {
    vaccini.territori.sort((a, b) => a.percentuale_popolazione_vaccinata > b.percentuale_popolazione_vaccinata ? 1 : -1);
    if (sort_by_name == true) {
      vaccini.territori.sort((a, b) => a.nome_territorio > b.nome_territorio ? 1 : -1);
    }
    data = vaccini.territori.filter(x => x.nome_territorio != "Italia").map(x => parseFloat(x.percentuale_popolazione_vaccinata).toFixed(2));
    labels = vaccini.territori.filter(x => x.nome_territorio != "Italia").map(x => x.nome_territorio);
    background_colors = data.map(x => `hsla(${x / 100 * 120}, 100%, 50%, 0.5)`);
    border_colors = data.map(x => `hsl(${x / 100 * 120}, 100%, 50%)`);
    hover_background_colors = data.map(x => `hsla(${x / 100 * 120}, 100%, 50%, 0.25)`);
    label = "Percentuale popolazione vaccinata";
  } else if (order === 2) {
    vaccini.territori.sort((a, b) => a.totale_dosi_consegnate > b.totale_dosi_consegnate ? 1 : -1);
    if (sort_by_name == true) {
      vaccini.territori.sort((a, b) => a.nome_territorio > b.nome_territorio ? 1 : -1);
    }
    data = vaccini.territori.filter(x => x.nome_territorio != "Italia").map(x => x.totale_dosi_consegnate);
    background_colors = data.map(x => `hsla(${x / Math.max(...data) * 120}, 100%, 50%, 0.5)`);
    border_colors = data.map(x => `hsl(${x / Math.max(...data) * 120}, 100%, 50%)`);
    hover_background_colors = data.map(x => `hsla(${x / Math.max(...data) * 120}, 100%, 50%, 0.25)`);
    labels = vaccini.territori.filter(x => x.nome_territorio != "Italia").map(x => x.nome_territorio);
    label = "Totale dosi di vaccino consegnate";
  }

  font_size = $(window).width() > 480 ? 12 : 8;
  if (old_chart) {
    // update the old chart
    old_chart.data = {
      labels: labels,
      datasets: [{
        data: data,
        label: label,
        backgroundColor: background_colors,
        borderColor: border_colors,
        borderWidth: 2,
        hoverBackgroundColor: hover_background_colors,
        hoverBorderColor: hover_background_colors
      }],
    };
    old_chart.update();
  } else {
    // draw the new chart
    let ctx = $("canvas#territori")[0].getContext('2d');
    chart = new Chart(ctx, {
        type: "bar",
        data: {
          labels: labels,
          datasets: [{
            data: data,
            label: label,
            backgroundColor: background_colors,
            borderColor: border_colors,
            borderWidth: 2,
            hoverBackgroundColor: hover_background_colors,
            hoverBorderColor: hover_background_colors
          }],
        },
        options: {
          responsive: true,
          aspectRatio: 1.1,
          legend: {
            align: "end"
          },
          tooltips: {
          },
          scales: {
            xAxes: [{
              ticks: {
                fontSize: font_size
              }
            }],
            yAxes: [{
              ticks: {
                fontSize: font_size
              }
            }]
          }
        }
    });
  }
  return chart;
};

// load data about each category
const load_categories = (order, reverse) => {
  if (order === 0) {
    vaccini.categorie.sort((a, b) => a.id_categoria > b.id_categoria ? 1 : -1);
  } else if (order === 1) {
    vaccini.categorie.sort((a, b) => a.totale_vaccinati > b.totale_vaccinati ? 1 : -1);
  }

  if (reverse) {
    vaccini.categorie.reverse();
  }

  $("table#categorie tbody").html("");

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
    $("table#categorie tbody").append(new_tr);
  });
};

const load_categories_chart = (order, old_chart) => {
  // chart variables
  let chart;
  let data;
  let label;
  let labels;
  let background_colors;
  let border_colors;
  let hover_background_colors;
  let font_size;

  // sort data and fill variables
  if (order === 0) {
    vaccini.categorie.sort((a, b) => a.id_categoria > b.id_categoria ? 1 : -1);
  } else if (order === 1) {
    vaccini.categorie.sort((a, b) => a.totale_vaccinati > b.totale_vaccinati ? 1 : -1);
  }

  data = vaccini.categorie.map(x => x.totale_vaccinati);
  background_colors = data.map(x => "#1e88e5");
  border_colors = data.map(x => "#005cb2");
  hover_background_colors = data.map(x => "#6ab7ff");
  labels = vaccini.categorie.map(x => x.nome_categoria.split(" "));
  label = "Totale vaccinati";

  font_size = $(window).width() > 480 ? 14 : 10;
  if (old_chart) {
    // update the old chart
    old_chart.data = {
      labels: labels,
      datasets: [{
        data: data,
        label: label,
        backgroundColor: background_colors,
        borderColor: border_colors,
        borderWidth: 2,
        hoverBackgroundColor: hover_background_colors,
        hoverBorderColor: hover_background_colors
      }],
    };
    old_chart.update();
  } else {
    // draw the new chart
    let ctx = $("canvas#categorie")[0].getContext('2d');
    chart = new Chart(ctx, {
        type: "horizontalBar",
        data: {
          labels: labels,
          datasets: [{
            data: data,
            label: label,
            backgroundColor: background_colors,
            borderColor: border_colors,
            borderWidth: 2,
            hoverBackgroundColor: hover_background_colors,
            hoverBorderColor: hover_background_colors
          }],
        },
        options: {
          responsive: true,
          aspectRatio: 1.1,
          legend: {
            align: "end"
          },
          tooltips: {
          },
          scales: {
            xAxes: [{
              ticks: {
                fontSize: font_size
              }
            }],
            yAxes: [{
              ticks: {
                fontSize: font_size
              }
            }]
          }
        }
    });
  }
  return chart;
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

  $("table#sesso tbody").html("");

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
    $("table#sesso tbody").append(new_tr);
  });
};


const load_genders_chart = () => {
  let chart;
  let data;
  let label;
  let labels;
  let background_colors;
  let border_colors;
  let hover_background_colors;
  let font_size;

  data = vaccini.sesso.map(x => x.totale_vaccinati);
  background_colors = vaccini.sesso.map(x => {
    if (x.nome_categoria === "donne") return "#d81b60";
    else return "#29b6f6";
  });
  border_colors = vaccini.sesso.map(x => {
    if (x.nome_categoria === "donne") return "#b4004e";
    else return "#0086c3";
  });
  hover_background_colors = vaccini.sesso.map(x => {
    if (x.nome_categoria === "donne") return "#ff77a9";
    else return "#80d6ff";
  });
  labels = vaccini.sesso.map(x => x.nome_categoria);
  label = "Totale vaccinati";

  font_size = $(window).width() > 480 ? 14 : 10;

  // draw the new chart
  let ctx = $("canvas#sesso")[0].getContext('2d');
  chart = new Chart(ctx, {
      type: "doughnut",
      data: {
        labels: labels,
        datasets: [{
          data: data,
          backgroundColor: background_colors,
          borderColor: border_colors,
          borderWidth: 2,
          hoverBackgroundColor: hover_background_colors,
          hoverBorderColor: hover_background_colors
        }],
      },
      options: {
        responsive: true,
        aspectRatio: 1,
        legend: {
          align: "end"
        },
        tooltips: {
        }
      }
  });

  return chart;

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

  $("table#fasce_eta tbody").html("");

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
    $("table#fasce_eta tbody").append(new_tr);
  });
};


const load_age_ranges_chart = (order, old_chart) => {
  // chart variables
  let chart;
  let data;
  let label;
  let labels;
  let background_colors;
  let border_colors;
  let hover_background_colors;
  let font_size;

  // sort data and fill variables
  if (order === 0) {
    vaccini.fasce_eta.sort((a, b) => a.nome_categoria > b.nome_categoria ? 1 : -1);
  } else if (order === 1) {
    vaccini.fasce_eta.sort((a, b) => a.totale_vaccinati > b.totale_vaccinati ? 1 : -1);
  }

  data = vaccini.fasce_eta.map(x => x.totale_vaccinati);
  background_colors = data.map(x => "#1e88e5");
  border_colors = data.map(x => "#005cb2");
  hover_background_colors = data.map(x => "#6ab7ff");
  labels = vaccini.fasce_eta.map(x => x.nome_categoria);
  label = "Totale vaccinati";

  font_size = $(window).width() > 480 ? 14 : 10;
  if (old_chart) {
    // update the old chart
    old_chart.data = {
      labels: labels,
      datasets: [{
        data: data,
        label: label,
        backgroundColor: background_colors,
        borderColor: border_colors,
        borderWidth: 2,
        hoverBackgroundColor: hover_background_colors,
        hoverBorderColor: hover_background_colors
      }],
    };
    old_chart.update();
  } else {
    // draw the new chart
    let ctx = $("canvas#fasce_eta")[0].getContext('2d');
    chart = new Chart(ctx, {
        type: "bar",
        data: {
          labels: labels,
          datasets: [{
            data: data,
            label: label,
            backgroundColor: background_colors,
            borderColor: border_colors,
            borderWidth: 2,
            hoverBackgroundColor: hover_background_colors,
            hoverBorderColor: hover_background_colors
          }],
        },
        options: {
          responsive: true,
          aspectRatio: 1.1,
          legend: {
            align: "end"
          },
          tooltips: {
          },
          scales: {
            xAxes: [{
              ticks: {
                fontSize: font_size
              }
            }],
            yAxes: [{
              ticks: {
                fontSize: font_size
              }
            }]
          }
        }
    });
  }
  return chart;
};


// main function
$(document).ready(() => {
  set_last_update();
  load_italy();
  load_territories(0, false);
  load_categories(0, false);
  load_genders(0, false);
  load_age_ranges(0, false);

  let territories_chart = load_territories_chart(0, false);
  let categories_chart = load_categories_chart(0);
  let genders_chart = load_genders_chart(0);
  let ages_ranges_chart = load_age_ranges_chart(0);

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

    // this is the id of the table we clicked on
    let table_id = $(this).parentsUntil("table").parent().attr("id");
    // once we know the class, we can update its data
    if (table_id === "territori") {
      load_territories(column, reverse);
    } else if (table_id === "categorie") {
      load_categories(column, reverse);
    } else if (table_id === "sesso") {
      load_genders(column, reverse);
    } else if (table_id === "fasce_eta") {
      load_age_ranges(column, reverse);
    }
  });

  $(".chartcontainer input").click(function() {
    // id of the corresponding chart
    let chart_id = $(this).parentsUntil(".form").parent().attr("id");

    if (chart_id === "territori") {
      let value, sort_by_name;

      // all radios
      let radios = $(this).parents().find(".chartcontainer#territori").find("input[type=\"radio\"]").toArray();

      radios.forEach((r, i) => {
        if ($(r).prop("checked")) {
          // all checked radios
          if (i < 3) {
            // if it's one of the first 3, then it's the value
            value = i;
          } else {
            // otherwise it's the sorting order
            sort_by_name = i == 3 ? false : true;
          }
        }
      });

      territories_chart = load_territories_chart(value, sort_by_name, territories_chart);
    } else if (chart_id === "categorie") {
      let value = parseInt($(this).val());
      categories_chart = load_categories_chart(value, categories_chart);
    } else if (chart_id === "fasce_eta") {
      let value = parseInt($(this).val());
      ages_ranges_chart = load_age_ranges_chart(value, ages_ranges_chart);
    }
  });
});
