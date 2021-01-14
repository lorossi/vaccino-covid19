// Made by Lorenzo Rossi
// https://www.lorenzoros.si - https://github.com/lorossi

/*jshint esversion: 8 */
/*jshint strict: false */

// request page via get method and return json
const get_data_json = (url, data) => {
  return $.ajax({
    url: url,
    type: 'GET',
    data: data,
    complete: (response) => response.responseJSON
  });
};


// update the data about the last vax update
const set_last_update = async () => {
  try {
    const response = await get_data_json("/get/last_updated");
    $(".update .stats").html(response.last_updated);
  } catch (err) {
    console.log(`Impossibile caricare l'ultimo aggiornamento. Errore ${err.message}`);
    return;
  }
};


// load selection form item for all time char
const load_selection = async () => {
  try {
    const response = await get_data_json("/get/lista_territori");

    let new_element = "";
    response.territori.forEach(t => {
      new_element += `<option value="${t}">${t}</option>`;
    });
    $(".alltimechartcontainer select#territori").append(new_element);

  } catch (err) {
    console.log(`Impossibile caricare i territori. Errore ${err.message}`);
    return;
  }
};


// load options for all time chart
const all_time_get_options = () => {
  let values = [];
  let groups = [];
  let territory;

  // chech all the checkbox
  let checkboxes = $(".alltimechartcontainer input[type=\"checkbox\"]").toArray();

  checkboxes.forEach((c, i) => {
    if ($(c).prop("checked")) {
      // keep track of the checked values
      values.push(parseInt($(c).val()));
      $(c).attr("disabled", false);
    } else {
      $(c).attr("disabled", true);
    }
  });

  if (values.includes(0) || values.includes(1)) {
    $(checkboxes[0]).attr("disabled", false);
    $(checkboxes[1]).attr("disabled", false);
  } else if (values.length === 0) {
    $(checkboxes).attr("disabled", false);
  }

  // now load the territory name
  territory = $(".alltimechartcontainer select").val();

  // update the text over the chart
  $(".alltimechartcontainer span#nome_territorio").html(territory);

  // pack the values into an object and return them
  return {
    values: values,
    territory: territory
  };
};

// load the table data about Italy as a whole
const load_italy = async () => {
  try {
    const italy = await get_data_json("/get/italy");

    // is the percentage over 100%?
    let over = parseFloat(italy.percentuale_dosi_utilizzate) > 95;
    // update the divs
    $(".italia #vaccinati").html(`${italy.totale_vaccinati}`);
    $(".italia #deltavaccinati").html(`${italy.nuovi_vaccinati}`);
    $(".italia #dosi").html(`${italy.totale_dosi_consegnate}`);
    $(".italia #deltadosi").html(`${italy.nuove_dosi_consegnate}`);
    $(".italia #percentualevaccinati").html(`${italy.percentuale_popolazione_vaccinata.toFixed(2)}%`);
    if (over) {
      $(".italia #percentualevacciniusati").html(`<span class="warning">${italy.percentuale_dosi_utilizzate.toFixed(2)}%</span>`);
    } else {
      $(".italia #percentualevacciniusati").html(`${italy.percentuale_dosi_utilizzate.toFixed(2)}%`);
    }

  } catch (err) {
    console.log(`Impossibile caricare dati sull'Italia. Errore ${err.message}`);
    return;
  }
};


// load chart about Italy
const load_italy_chart = async (values, territory_name, old_obj) => {
  let chart;
  let labels = []; // x axis
  let datasets = [];
  let type;
  let old_chart;
  let history_data;

  try {
    old_obj = await old_obj;

    if (old_obj) {
      old_chart = old_obj.chart;
      history_data = old_obj.data;
    } else {
      history_data = await get_data_json("get/storico_vaccini");
    }

    // pack the values into array
    if (values === undefined) {
      values = [0];
    } else if (values.length === 0) {
      // no parameters sent
      // destroy old chart
      old_chart.destroy();
      return {
        chart: null,
        data: history_data
      };
    }

    if (territory_name === undefined) {
      territory_name = "Italia";
    }

    // dates as labels
    labels = history_data.map(x => x.script_timestamp);

    // multiple lines into datasets
    if (values.includes(0)) {
      let data = [];
      let label;
      history_data.forEach((a, i) => {
        label = "Totale vaccinati";
        let y;
        y = a.assoluti.filter(x => x.nome_territorio === territory_name)[0].totale_vaccinati;
        data.push({
          x: labels[i],
          y: y
        });
      });

      datasets.push({
        data: data,
        label: label,
        backgroundColor: `rgba(0, 0, 0, 0)`,
        borderColor: "#4caf50",
        hoverBackgroundColor: `rgba(0, 0, 0, 0)`,
      });

      type = "line";
    }

    if (values.includes(1)) {
      let data = [];
      let label;
      history_data.forEach((a, i) => {
        label = "Dosi Disponibili";
        let y;
        y = a.assoluti.filter(x => x.nome_territorio === territory_name)[0].totale_dosi_consegnate;
        data.push({
          x: labels[i],
          y: y
        });
      });

      datasets.push({
        data: data,
        label: label,
        backgroundColor: `rgba(0, 0, 0, 0)`,
        borderColor: "#2196f3",
        hoverBackgroundColor: `rgba(0, 0, 0, 0)`,
      });

      type = "line";
    }

    if (values.includes(2)) {
      let data = [];
      let label;
      history_data.forEach((v, i) => {
        label = "Vaccinati oggi";
        let y;
        y = v.variazioni.filter(x => x.nome_territorio === territory_name)[0].nuovi_vaccinati;
        data.push({
          x: labels[i],
          y: y
        });
      });

      datasets.push({
        data: data,
        label: label,
        backgroundColor: "#ffeb3b",
        borderColor: "#c9bc1f",
        borderWidth: 2,
        hoverBackgroundColor: "#ffff72",
        hoverBorderColor: "#ffff72"
      });

      type = "bar";
    }

    if (values.includes(3)) {
      let data = [];
      let label;
      history_data.forEach((a, i) => {
        label = "Percentuale vaccinata";
        let y;
        y = a.assoluti.filter(x => x.nome_territorio === territory_name)[0].percentuale_popolazione_vaccinata;
        data.push({
          x: labels[i],
          y: y
        });
      });

      datasets.push({
        data: data,
        label: label,
        backgroundColor: `rgba(0, 0, 0, 0)`,
        borderColor: "#ff5722",
        hoverBackgroundColor: `rgba(0, 0, 0, 0)`,
      });

      type = "line";
    }

    // font size and aspect ratio must me different on small screens
    let font_size = $(window).width() > 1500 ? 16 : 8;
    let aspect_ratio = $(window).width() > 480 ? 2.25 : 0.8;

    if (old_chart) {
      old_chart.data = {
        labels: labels,
        datasets: datasets
      };
      await old_chart.update();
      return {
        chart: old_chart,
        data: history_data
      };
    } else {
      let ctx = $("canvas#italia")[0].getContext('2d');
      chart = await new Chart(ctx, {
        type: type,
        data: {
          labels: labels,
          datasets: datasets
        },
        options: {
          aspectRatio: aspect_ratio,
          scales: {
            xAxes: [{
              ticks: {
                fontSize: font_size,
                autoSkip: false,
                maxRotation: 90,
                minRotation: 45,
              }
            }],
            yAxes: [{
              ticks: {
                fontSize: font_size,
                autoSkip: true,
                maxRotation: 30,
                minRotation: -30,
              }
            }]
          },
          legend: {
            align: "end",
            font_size: font_size
          },
          elements: {
            line: {
              cubicInterpolationMode: "monotone"
            }
          }
        }
      });
      return {
        chart: chart,
        data: history_data
      };
    }
  } catch (err) {
    console.log(`Impossibile caricare il grafico storico. Errore ${err.message}`);
    return;
  }
};


// load data about each territory
const load_territories = async (order, reverse, territories) => {
  try {
    territories = await territories;
    if (!territories) territories = await get_data_json("/get/territori");
    // sort data
    if (order === 0) {
      territories.sort((a, b) => a.nome_territorio > b.nome_territorio ? 1 : -1);
    } else if (order === 1) {
      territories.sort((a, b) => a.totale_vaccinati > b.totale_vaccinati ? 1 : -1);
    } else if (order === 2) {
      territories.sort((a, b) => a.percentuale_popolazione_vaccinata > b.percentuale_popolazione_vaccinata ? 1 : -1);
    } else if (order === 3) {
      territories.sort((a, b) => a.totale_dosi_consegnate > b.totale_dosi_consegnate ? 1 : -1);
    } else if (order === 4) {
      territories.sort((a, b) => a.percentuale_dosi_utilizzate > b.percentuale_dosi_utilizzate ? 1 : -1);
    }

    if (reverse) {
      territories.reverse();
    }

    // fill table
    $("table#territori tbody").html("");

    territories.forEach((t, i) => {
      let nome_territorio_corto;
      if (t.codice_territorio === "06") {
        nome_territorio_corto = "E.R.";
      } else if (t.codice_territorio === "07") {
        nome_territorio_corto = "F.V.G";
      } else if (t.codice_territorio === "20") {
        nome_territorio_corto = "V. d'Aosta";
      } else {
        nome_territorio_corto = t.nome_territorio;
      }

      let percentuale_vaccinati;
      percentuale_vaccinati = `${parseFloat(t.percentuale_popolazione_vaccinata).toFixed(2)}%`;
      let percentuale_dosi;
      percentuale_dosi = `${parseFloat(t.percentuale_dosi_utilizzate).toFixed(2)}%`;
      let over = t.percentuale_dosi_utilizzate > 100;

      let new_tr = `<tr id="${t.codice_territorio}" class="territorio">`;
      new_tr += `<td><span class="mobile">${nome_territorio_corto}</span><span class="pc">${t.nome_territorio}</span></td>`;
      new_tr += `<td>${t.totale_vaccinati}`;
      new_tr += `<td>${percentuale_vaccinati}</td>`;
      new_tr += `<td>${t.totale_dosi_consegnate}`;
      if (over) {
        new_tr += `<td><span class="warning">${percentuale_dosi}</span>`;
      } else {
        new_tr += `<td>${percentuale_dosi}`;
      }

      new_tr += "</tr>";
      $("table#territori tbody").append(new_tr);
    });

    return territories;
  } catch (err) {
    console.log(`Impossibile caricare dati sui territori. Errore ${err.message}`);
    return;
  }
};


const load_territories_chart = async (order, sort_by_name, old_obj) => {
  // chart variables
  let chart;
  let data;
  let label;
  let labels;
  let background_colors;
  let border_colors;
  let hover_background_colors;
  let font_size;
  let old_chart;
  let territories;


  try {
    old_obj = await old_obj;

    if (old_obj) {
      old_chart = old_obj.chart;
      territories = old_obj.data;
    } else {
      territories = await get_data_json("get/territori");
    }

    // sort data and fill variables
    if (order === 0) {
      territories.sort((a, b) => a.totale_vaccinati > b.totale_vaccinati ? 1 : -1);
      if (sort_by_name) {
        territories.sort((a, b) => a.nome_territorio > b.nome_territorio ? 1 : -1);
      }
      data = territories.filter(x => x.nome_territorio != "Italia").map(x => x.totale_vaccinati);
      background_colors = data.map(x => `hsla(${x / Math.max(...data) * 120}, 100%, 50%, 0.5)`);
      border_colors = data.map(x => `hsl(${x / Math.max(...data) * 120}, 100%, 50%)`);
      hover_background_colors = data.map(x => `hsla(${x / Math.max(...data) * 120}, 100%, 50%, 0.25)`);
      labels = territories.filter(x => x.nome_territorio != "Italia").map(x => x.nome_territorio);
      label = "Totale vaccinati";
    } else if (order === 1) {
      territories.sort((a, b) => a.percentuale_popolazione_vaccinata > b.percentuale_popolazione_vaccinata ? 1 : -1);
      if (sort_by_name) {
        territories.sort((a, b) => a.nome_territorio > b.nome_territorio ? 1 : -1);
      }
      data = territories.filter(x => x.nome_territorio != "Italia").map(x => parseFloat(x.percentuale_popolazione_vaccinata).toFixed(2));
      labels = territories.filter(x => x.nome_territorio != "Italia").map(x => x.nome_territorio);
      background_colors = data.map(x => `hsla(${x / 100 * 120}, 100%, 50%, 0.5)`);
      border_colors = data.map(x => `hsl(${x / 100 * 120}, 100%, 50%)`);
      hover_background_colors = data.map(x => `hsla(${x / 100 * 120}, 100%, 50%, 0.25)`);
      label = "Percentuale popolazione vaccinata";
    } else if (order === 2) {
      territories.sort((a, b) => a.totale_dosi_consegnate > b.totale_dosi_consegnate ? 1 : -1);
      if (sort_by_name) {
        territories.sort((a, b) => a.nome_territorio > b.nome_territorio ? 1 : -1);
      }
      data = territories.filter(x => x.nome_territorio != "Italia").map(x => x.totale_dosi_consegnate);
      background_colors = data.map(x => `hsla(${x / Math.max(...data) * 120}, 100%, 50%, 0.5)`);
      border_colors = data.map(x => `hsl(${x / Math.max(...data) * 120}, 100%, 50%)`);
      hover_background_colors = data.map(x => `hsla(${x / Math.max(...data) * 120}, 100%, 50%, 0.25)`);
      labels = territories.filter(x => x.nome_territorio != "Italia").map(x => x.nome_territorio);
      label = "Totale dosi di vaccino consegnate";
    } else if (order === 3) {
      territories.sort((a, b) => a.percentuale_dosi_utilizzate > b.percentuale_dosi_utilizzate ? 1 : -1);
      if (sort_by_name) {
        territories.sort((a, b) => a.nome_territorio > b.nome_territorio ? 1 : -1);
      }
      data = territories.filter(x => x.nome_territorio != "Italia").map(x => x.percentuale_dosi_utilizzate.toFixed(2));
      background_colors = data.map(x => `hsla(${120 - x / 100 * 120}, 100%, 50%, 0.5)`);
      border_colors = data.map(x => `hsl(${120 - x / Math.max(...data) * 120}, 100%, 50%)`);
      hover_background_colors = data.map(x => `hsla(${120 - x /100 * 120}, 100%, 50%, 0.25)`);
      labels = territories.filter(x => x.nome_territorio != "Italia").map(x => x.nome_territorio);
      label = "Percentuale vaccini utlizzati";
    }

    // calculate average
    let average = data.reduce((sum, d) => parseFloat(sum) + parseFloat(d)) / data.length;
    if (average > 100) {
      average = parseInt(average);
    } else {
      average = average.toFixed(2);
    }

    font_size = $(window).width() > 1500 ? 12 : 8;
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
        }, {
          label: 'Media',
          labels: new Array(data.length).fill("media"),
          data: new Array(data.length).fill(average),
          type: 'line',
          backgroundColor: "hsla(0, 100%, 50%, 0.05)",
          borderColor: "hsl(0, 100%, 50%)",
          pointRadius: 0,
          borderWidth: 1
        }],
      };
      old_chart.update();
      return {
        chart: old_chart,
        data: territories
      };
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
          }, {
            label: 'Media',
            labels: new Array(data.length).fill("media"),
            data: new Array(data.length).fill(parseInt(average)),
            type: 'line',
            backgroundColor: "hsla(0, 100%, 50%, 0.05)",
            borderColor: "hsl(0, 100%, 50%)",
            pointRadius: 0,
            borderWidth: 1
          }],
        },
        options: {
          responsive: true,
          aspectRatio: 1.1,
          legend: {
            align: "end"
          },
          tooltips: {},
          scales: {
            xAxes: [{
              ticks: {
                autoSkip: false,
                maxRotation: 90,
                minRotation: 45,
                fontSize: font_size
              }
            }],
            yAxes: [{
              ticks: {
                fontSize: font_size,
                autoSkip: true,
                maxRotation: 30,
                minRotation: -30,
              }
            }]
          }
        }
      });
      return {
        chart: chart,
        data: territories
      };
    }
  } catch (err) {
    console.log(`Impossibile caricare il grafico dei territori. Errore ${err.message}`);
    return;
  }
};


const load_variations = async (order, reverse, variations) => {
  try {
    variations = await variations;
    if (!variations) variations = await get_data_json("/get/variazioni");

    // sort data
    if (order === 0) {
      variations.sort((a, b) => a.nome_territorio > b.nome_territorio ? 1 : -1);
    } else if (order === 1) {
      variations.sort((a, b) => a.nuovi_vaccinati > b.nuovi_vaccinati ? 1 : -1);
    } else if (order === 2) {
      variations.sort((a, b) => a.percentuale_nuovi_vaccinati > b.percentuale_nuovi_vaccinati ? 1 : -1);
    } else if (order === 3) {
      variations.sort((a, b) => a.nuove_dosi_consegnate > b.nuove_dosi_consegnate ? 1 : -1);
    } else if (order === 4) {
      variations.sort((a, b) => a.percentuale_nuove_dosi_consegnate > b.percentuale_nuove_dosi_consegnate ? 1 : -1);
    }

    if (reverse) {
      variations.reverse();
    }

    // fill table
    $("table#variazioni tbody").html("");

    variations.forEach((t, i) => {
      let nome_territorio_corto;
      if (t.codice_territorio === "06") {
        nome_territorio_corto = "E.R.";
      } else if (t.codice_territorio === "07") {
        nome_territorio_corto = "F.V.G";
      }

      let new_tr = `<tr id="${t.codice_territorio}" class="territorio">`;
      if (nome_territorio_corto) {
        new_tr += `<td><span class="pc">${t.nome_territorio}</span><span class="mobile">${nome_territorio_corto}</span></td>`;
      } else {
        new_tr += `<td>${t.nome_territorio}</td>`;
      }

      new_tr += `<td>+${t.nuovi_vaccinati}`;
      new_tr += `<td>+${t.percentuale_nuovi_vaccinati.toFixed(2)}%</td>`;
      new_tr += `<td>+${t.nuove_dosi_consegnate}`;
      new_tr += `<td>+${t.percentuale_nuove_dosi_consegnate.toFixed(2)}%</td>`;
      new_tr += "</tr>";
      $("table#variazioni tbody").append(new_tr);
    });
    return variations;
  } catch (err) {
    console.log(`Impossibile caricare dati sulle variazioni. Errore ${err.message}`);
    return;
  }
};


const load_variations_chart = async (order, sort_by_name, old_obj) => {
  // chart variables
  let chart;
  let data;
  let label;
  let labels;
  let background_colors;
  let border_colors;
  let hover_background_colors;
  let font_size;
  let old_chart;
  let variations;

  try {
    old_obj = await old_obj;
    if (old_obj) {
      old_chart = old_obj.chart;
      variations = old_obj.data;
    } else {
      variations = await get_data_json("/get/variazioni");
    }

    // sort data and fill variables
    if (order === 0) {
      variations.sort((a, b) => a.nuovi_vaccinati > b.nuovi_vaccinati ? 1 : -1);
      if (sort_by_name) {
        variations.sort((a, b) => a.nome_territorio > b.nome_territorio ? 1 : -1);
      }
      data = variations.filter(x => x.nome_territorio != "Italia").map(x => x.nuovi_vaccinati);
      label = "Nuovi vaccinati";
    } else if (order === 1) {
      variations.sort((a, b) => a.percentuale_nuovi_vaccinati > b.percentuale_nuovi_vaccinati ? 1 : -1);
      if (sort_by_name) {
        variations.sort((a, b) => a.nome_territorio > b.nome_territorio ? 1 : -1);
      }
      data = variations.filter(x => x.nome_territorio != "Italia").map(x => x.percentuale_nuovi_vaccinati.toFixed(2));
      label = "Variazione nuovi vaccinati";
    } else if (order === 2) {
      variations.sort((a, b) => a.nuove_dosi_consegnate > b.nuove_dosi_consegnate ? 1 : -1);
      if (sort_by_name) {
        variations.sort((a, b) => a.nome_territorio > b.nome_territorio ? 1 : -1);
      }
      data = variations.filter(x => x.nome_territorio != "Italia").map(x => x.nuove_dosi_consegnate);
      label = "Nuovi vaccini";
    } else if (order === 3) {
      variations.sort((a, b) => a.percentuale_nuove_dosi_consegnate > b.percentuale_nuove_dosi_consegnate ? 1 : -1);
      if (sort_by_name) {
        variations.sort((a, b) => a.nome_territorio > b.nome_territorio ? 1 : -1);
      }
      data = variations.filter(x => x.nome_territorio != "Italia").map(x => x.percentuale_nuove_dosi_consegnate.toFixed(2));
      label = "Variazione nuovi vaccini";
    }

    background_colors = data.map(x => `hsla(${x / Math.max(...data) * 120}, 100%, 50%, 0.5)`);
    border_colors = data.map(x => `hsl(${x / Math.max(...data) * 120}, 100%, 50%)`);
    hover_background_colors = data.map(x => `hsla(${x / Math.max(...data) * 120}, 100%, 50%, 0.25)`);
    labels = variations.filter(x => x.nome_territorio != "Italia").map(x => x.nome_territorio);

    // calculate average
    let average = data.reduce((sum, d) => parseFloat(sum) + parseFloat(d)) / data.length;

    // round average
    if (average > 100) {
      average = parseInt(average);
    } else {
      average = average.toFixed(2);
    }

    font_size = $(window).width() > 1500 ? 12 : 8;
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
        }, {
          label: 'Media',
          labels: new Array(data.length).fill("media"),
          data: new Array(data.length).fill(average),
          type: 'line',
          backgroundColor: "hsla(0, 100%, 50%, 0.05)",
          borderColor: "hsl(0, 100%, 50%)",
          pointRadius: 0,
          borderWidth: 1
        }],
      };
      old_chart.update();
      return {
        chart: old_chart,
        data: variations
      };
    } else {
      // draw the new chart
      let ctx = $("canvas#variazioni")[0].getContext('2d');
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
          }, {
            label: 'Media',
            labels: new Array(data.length).fill("media"),
            data: new Array(data.length).fill(average),
            type: 'line',
            backgroundColor: "hsla(0, 100%, 50%, 0.05)",
            borderColor: "hsl(0, 100%, 50%)",
            pointRadius: 0,
            borderWidth: 1
          }],
        },
        options: {
          responsive: true,
          aspectRatio: 1.1,
          legend: {
            align: "end"
          },
          tooltips: {},
          scales: {
            xAxes: [{
              ticks: {
                autoSkip: false,
                maxRotation: 90,
                minRotation: 45,
                fontSize: font_size
              }
            }],
            yAxes: [{
              ticks: {
                fontSize: font_size,
                autoSkip: true,
                maxRotation: 30,
                minRotation: -30,
              }
            }]
          }
        }
      });
      return {
        chart: chart,
        data: variations
      };
    }
  } catch (err) {
    console.log(`Impossibile caricare il grafico delle variazioni. Errore ${err.message}`);
    return;
  }
};

// load data about each category
const load_categories = async (order, reverse, categories) => {
  try {
    categories = await categories;
    if (!categories) categories = await get_data_json("/get/categorie");
    // sort
    if (order === 0) {
      categories.sort((a, b) => a.id_categoria > b.id_categoria ? 1 : -1);
    } else if (order === 1) {
      categories.sort((a, b) => a.totale_vaccinati > b.totale_vaccinati ? 1 : -1);
    } else if (order === 2) {
      categories.sort((a, b) => a.nuovi_vaccinati > b.nuovi_vaccinati ? 1 : -1);
    } else if (order === 3) {
      categories.sort((a, b) => a.percentuale_nuovi_vaccinati > b.percentuale_nuovi_vaccinati ? 1 : -1);
    }

    if (reverse) {
      categories.reverse();
    }

    $("table#categorie tbody").html("");

    categories.forEach((t, i) => {
      let nuovi_vaccinati;
      let percentuale_nuovi_vaccinati;
      if (t.nuovi_vaccinati === undefined) {
        nuovi_vaccinati = 0;
        percentuale_nuovi_vaccinati = 0;
      } else {
        nuovi_vaccinati = t.nuovi_vaccinati;
        percentuale_nuovi_vaccinati = t.percentuale_nuovi_vaccinati;
      }

      let new_tr = `<tr id="${t.id_categoria}" class="categorie">`;
      new_tr += `<td>${t.nome_categoria}</td>`;
      new_tr += `<td>${t.totale_vaccinati}</td>`;
      new_tr += `<td>+${nuovi_vaccinati}</td>`;
      new_tr += `<td>+${percentuale_nuovi_vaccinati.toFixed(2)}%</td>`;
      new_tr += "</tr>";
      $("table#categorie tbody").append(new_tr);
    });
    return categories;
  } catch (err) {
    console.log(`Impossibile caricare le categorie. Errore ${err.message}`);
    return;
  }
};


const load_categories_chart = async (order, old_obj) => {
  // chart variables
  let chart;
  let data;
  let label;
  let labels;
  let background_colors;
  let border_colors;
  let hover_background_colors;
  let font_size;
  let old_chart;
  let categories;

  try {
    old_obj = await old_obj;

    if (old_obj) {
      old_chart = old_obj.chart;
      categories = old_obj.data;
    } else {
      categories = await get_data_json("/get/categorie");
    }

    // sort data and fill variables
    if (order === 0) {
      categories.sort((a, b) => a.id_categoria > b.id_categoria ? 1 : -1);
    } else if (order === 1) {
      categories.sort((a, b) => a.totale_vaccinati > b.totale_vaccinati ? 1 : -1);
    }

    data = categories.map(x => x.totale_vaccinati);
    background_colors = data.map(x => "#1e88e5");
    border_colors = data.map(x => "#005cb2");
    hover_background_colors = data.map(x => "#6ab7ff");
    labels = categories.map(x => x.nome_categoria.split(" "));
    label = "Totale vaccinati";

    font_size = $(window).width() > 1500 ? 14 : 10;
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
      return {
        chart: old_chart,
        data: categories
      };
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
          tooltips: {},
          scales: {
            xAxes: [{
              ticks: {
                autoSkip: false,
                maxRotation: 90,
                minRotation: 45,
                fontSize: font_size
              }
            }],
            yAxes: [{
              ticks: {
                fontSize: font_size,
                autoSkip: true,
              }
            }]
          }
        }
      });
      return {
        chart: chart,
        data: categories
      };
    }
  } catch (err) {
    console.log(`Impossibile caricare il grafico delle categorie. Errore ${err.message}`);
    return;
  }
};


// load data about each gender
const load_genders = async (order, reverse, genders) => {
  try {
    genders = await genders;
    if (!genders) genders = await get_data_json("/get/sessi");

    if (order === 0) {
      genders.sort((a, b) => a.nome_categoria > b.nome_categoria ? 1 : -1);
    } else if (order === 1) {
      genders.sort((a, b) => a.totale_vaccinati > b.totale_vaccinati ? 1 : -1);
    } else if (order === 2) {
      genders.sort((a, b) => a.nuovi_vaccinati > b.nuovi_vaccinati ? 1 : -1);
    } else if (order === 3) {
      genders.sort((a, b) => a.percentuale_nuovi_vaccinati > b.percentuale_nuovi_vaccinati ? 1 : -1);
    }

    if (reverse) {
      genders.reverse();
    }

    $("table#sesso tbody").html("");

    genders.forEach((t, i) => {
      let new_tr = `<tr id="${t.nome_categoria}" class="sesso">`;
      new_tr += `<td>${t.nome_categoria}</td>`;
      new_tr += `<td>${t.totale_vaccinati}</td>`;
      new_tr += `<td>+${t.nuovi_vaccinati}</td>`;
      new_tr += `<td>+${t.percentuale_nuovi_vaccinati.toFixed(2)}%</td>`;
      new_tr += "</tr>";
      $("table#sesso tbody").append(new_tr);
    });

    return genders;
  } catch (err) {
    console.log(`Impossibile caricare i sessi. Errore ${err.message}`);
    return;
  }
};


const load_genders_chart = async (genders) => {
  let chart;
  let data;
  let label;
  let labels;
  let background_colors;
  let border_colors;
  let hover_background_colors;
  let font_size;

  try {
    genders = await genders;
    if (!genders) genders = await get_data_json("/get/sessi");
    data = genders.map(x => x.totale_vaccinati);
    background_colors = genders.map(x => {
      if (x.nome_categoria === "donne") return "#d81b60";
      else return "#29b6f6";
    });
    border_colors = genders.map(x => {
      if (x.nome_categoria === "donne") return "#b4004e";
      else return "#0086c3";
    });
    hover_background_colors = genders.map(x => {
      if (x.nome_categoria === "donne") return "#ff77a9";
      else return "#80d6ff";
    });
    labels = genders.map(x => x.nome_categoria);
    label = "Totale vaccinati";

    font_size = $(window).width() > 1500 ? 14 : 10;

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
        tooltips: {}
      }
    });
    return chart;
  } catch (err) {
    console.log(`Impossibile caricare il grafico dei sessi. Errore ${err.message}`);
    return;
  }
};

// load data about age ranges
const load_age_ranges = async (order, reverse, age_ranges) => {
  try {
    age_ranges = await age_ranges
    if (!age_ranges) age_ranges = await get_data_json("/get/fasce_eta");

    if (order === 0) {
      age_ranges.sort((a, b) => a.nome_categoria > b.nome_categoria ? 1 : -1);
    } else if (order === 1) {
      age_ranges.sort((a, b) => a.totale_vaccinati > b.totale_vaccinati ? 1 : -1);
    } else if (order === 2) {
      age_ranges.sort((a, b) => a.nuovi_vaccinati > b.nuovi_vaccinati ? 1 : -1);
    } else if (order === 3) {
      age_ranges.sort((a, b) => a.percentuale_nuovi_vaccinati > b.percentuale_nuovi_vaccinati ? 1 : -1);
    }

    if (reverse) {
      age_ranges.reverse();
    }

    $("table#fasce_eta tbody").html("");

    age_ranges.forEach((t, i) => {
      let nuovi_vaccinati = t.nuovi_vaccinati || t.totale_vaccinati;
      let percentuale_nuovi_vaccinati = t.percentuale_nuovi_vaccinati || 100;

      let new_tr = `<tr id="${t.nome_categoria}" class="territorio">`;
      new_tr += `<td>${t.nome_categoria}</td>`;
      new_tr += `<td>${t.totale_vaccinati}</td>`;
      new_tr += `<td>+${nuovi_vaccinati}</td>`;
      new_tr += `<td>+${percentuale_nuovi_vaccinati.toFixed(2)}%</td>`;
      new_tr += "</tr>";
      $("table#fasce_eta tbody").append(new_tr);
    });

    return age_ranges;
  } catch (err) {
    console.log(`Impossibile caricare le fasce di età. Errore ${err.message}`);
    return;
  }
};


const load_age_ranges_chart = async (order, old_obj) => {
  // chart variables
  let chart;
  let data;
  let label;
  let labels;
  let background_colors;
  let border_colors;
  let hover_background_colors;
  let font_size;
  let old_chart;
  let ages_ranges;

  try {
    old_obj = await old_obj;

    if (old_obj) {
      old_chart = old_obj.chart;
      age_ranges = old_obj.data;
    } else {
      age_ranges = await get_data_json("/get/fasce_eta");
    }

    // sort data and fill variables
    if (order === 0) {
      age_ranges.sort((a, b) => a.nome_categoria > b.nome_categoria ? 1 : -1);
    } else if (order === 1) {
      age_ranges.sort((a, b) => a.totale_vaccinati > b.totale_vaccinati ? 1 : -1);
    }

    data = age_ranges.map(x => x.totale_vaccinati);
    background_colors = data.map(x => "#1e88e5");
    border_colors = data.map(x => "#005cb2");
    hover_background_colors = data.map(x => "#6ab7ff");
    labels = age_ranges.map(x => x.nome_categoria);
    label = "Totale vaccinati";

    font_size = $(window).width() > 1500 ? 14 : 10;
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
      return {
        chart: old_chart,
        data: age_ranges
      };
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
          tooltips: {},
          scales: {
            xAxes: [{
              ticks: {
                autoSkip: false,
                maxRotation: 90,
                minRotation: 45,
                fontSize: font_size
              }
            }],
            yAxes: [{
              ticks: {
                fontSize: font_size,
                autoSkip: true,
                maxRotation: 30,
                minRotation: -30,
              }
            }]
          }
        }
      });
      return {
        chart: chart,
        data: age_ranges
      };
    }
  } catch (err) {
    console.log(`Impossibile caricare il grafico delle fasce di età. Errore ${err.message}`);
    return;
  }
};

// main function
$(document).ready(async () => {
  console.log("Snooping around? Check the repo instead! https://github.com/lorossi/vaccino-covid19");
  // load basic infos
  set_last_update();
  load_selection();
  load_italy();
  // load tables
  let territories = load_territories(0, false);
  let variations = load_variations(0, false);
  let categories = load_categories(0, false);
  let genders = load_genders(0, false);
  let age_ranges = load_age_ranges(0, false);

  // global charts variables
  Chart.defaults.global.defaultFontFamily = 'Roboto';
  // load charts and keep the variable
  let italy_chart = load_italy_chart([0, 1], "Italia");
  let territories_chart = load_territories_chart(0, false, {
    data: await territories
  });
  let variations_chart = load_variations_chart(0, false, {
    data: await variations
  });
  let categories_chart = load_categories_chart(0, {
    data: await categories
  });
  let genders_chart = load_genders_chart(await genders);
  let ages_ranges_chart = load_age_ranges_chart(0, {
    data: await age_ranges
  });

  // form for all time chart
  $(".alltimechartcontainer input[type=\"checkbox\"]").click(() => {
    let options = all_time_get_options();
    italy_chart = load_italy_chart(options.values, options.territory, italy_chart);
  });

  // dropdown for all time chart
  $(".alltimechartcontainer select").on("change", () => {
    let options = all_time_get_options();
    italy_chart = load_italy_chart(options.values, options.territory, italy_chart);
  });

  // sorting for tables
  $("table th").click((e) => {
    // get column id
    let column = $(e.target).data("column");
    // should the data be reversed?
    let reverse;
    // up/down sorting management. It is handled with a class
    if ($(e.target).hasClass("darr")) {
      reverse = true;
      $(e.target).removeClass("darr");
      $(e.target).addClass("uarr");
    } else {
      reverse = false;
      $(e.target).removeClass("uarr");
      $(e.target).addClass("darr");
    }

    // this is the id of the table we clicked on
    let table_id = $(e.target).parentsUntil("table").parent().attr("id");

    // once we know the class, we can update its data
    if (table_id === "territori") {
      load_territories(column, reverse, territories);
    } else if (table_id === "variazioni") {
      load_variations(column, reverse, variations);
    } else if (table_id === "categorie") {
      load_categories(column, reverse, categories);
    } else if (table_id === "sesso") {
      load_genders(column, reverse, genders);
    } else if (table_id === "fasce_eta") {
      load_age_ranges(column, reverse, age_ranges);
    }
  });

  // this function won't work with arrow
  $(".chartcontainer input").click((e) => {
    // id of the corresponding chart
    // ugly but works i guess
    let chart_id = $(e.target).closest(".chartcontainer").attr("id");
    if (chart_id === "territori") {
      let value, sort_by_name;
      // all radios
      let radios = $(e.target).parents().find(".chartcontainer#territori").find("input[type=\"radio\"]").toArray();

      radios.forEach((r, i) => {
        if ($(r).prop("checked")) {
          // all checked radios
          if (i < 4) {
            // if it's one of the first 3, then it's the value
            value = i;
          } else {
            // otherwise it's the sorting order
            sort_by_name = i == 4 ? false : true;
          }
        }
      });

      territories_chart = load_territories_chart(value, sort_by_name, territories_chart);
    } else if (chart_id === "variazioni") {
      let value, sort_by_name;
      // all radios
      let radios = $(e.target).parents().find(".chartcontainer#variazioni").find("input[type=\"radio\"]").toArray();

      radios.forEach((r, i) => {
        if ($(r).prop("checked")) {
          // all checked radios
          if (i < 4) {
            // if it's one of the first 3, then it's the value
            value = i;
          } else {
            // otherwise it's the sorting order
            sort_by_name = i == 4 ? false : true;
          }
        }
      });

      variations_chart = load_variations_chart(value, sort_by_name, variations_chart);

    } else if (chart_id === "categorie") {
      let value = parseInt($(e.target).val());
      categories_chart = load_categories_chart(value, categories_chart);
    } else if (chart_id === "fasce_eta") {
      let value = parseInt($(e.target).val());
      ages_ranges_chart = load_age_ranges_chart(value, ages_ranges_chart);
    }
  });
});
