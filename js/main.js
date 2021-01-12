// Made by Lorenzo Rossi
// https://www.lorenzoros.si - https://github.com/lorossi

/*jshint esversion: 8 */
/*jshint strict: false */


// update the data about the last vax update
const set_last_update = () => {
  $(".update .stats").html(vaccini.last_updated);
};


// load selection form item for all time char
const load_selection = () => {
  let new_element = "";
  storico_vaccini[0].territori.forEach((t, i) => {
    let new_option = `<option value="${t.nome_territorio}">${t.nome_territorio}</option>`;
    // if we have a territory code, append it to the end (it's a territory)
    if (t.codice_territorio) new_element += new_option;
    // otherwise, prepend it (it's italy as a whole)
    else new_element = new_option + new_element;
  });

  $(".alltimechartcontainer select#territori").append(new_element);
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
  $(".alltimechartcontainer span#nome_territorio").text(territory);

  // pack the values into an object and return them
  return {
    values: values,
    territory: territory
  };
};


// load the table data about Italy as a whole
const load_italy = () => {
  // copy array, so whule filtering it we don't alter it
  // sorting is ok tho
  [...vaccini.territori].filter(x => x.nome_territorio === "Italia").forEach((t, i) => {
    // due to a change, new vaccined  might not always be present
    let nuovi_vaccinati;
    if (t.nuovi_vaccinati === undefined) {
      nuovi_vaccinati = 0;
    } else {
      nuovi_vaccinati = t.nuovi_vaccinati;
    }
    // same for new doses
    let nuove_dosi;
    if (t.nuove_dosi_consegnate === undefined) {
      nuove_dosi = 0;
    } else {
      nuove_dosi = t.nuove_dosi_consegnate;
    }

    // update the divs
    $(".italia #vaccinati").text(`${t.totale_vaccinati}`);
    $(".italia #deltavaccinati").text(`${nuovi_vaccinati}`);
    $(".italia #dosi").text(`${t.totale_dosi_consegnate}`);
    $(".italia #deltadosi").text(`${nuove_dosi}`);
    $(".italia #percentualevaccinati").text(`${t.percentuale_popolazione_vaccinata.toFixed(2)}%`);
    $(".italia #percentualevacciniusati").text(`${t.percentuale_dosi_utilizzate.toFixed(2)}%`);

    return;
  });
};


// load chart about Italy
const load_italy_chart = (values, territory_name, old_chart) => {
  let chart;
  let labels = []; // x axis
  let datasets = [];
  let type;

  // pack the values into array
  if (values === undefined) {
    values = [0];
  } else if (values.length === 0) {
    // no parameters sent
    // destroy old chart
    old_chart.destroy();
    return;
  }

  if (territory_name === undefined) {
    territory_name = "Italia";
  }

  // dates as labels
  labels = storico_vaccini.map(x => x.script_timestamp);

  // multiple lines into datasets
  if (values.includes(0)) {
    let data = [];
    let label;
    [...storico_vaccini].forEach((s, i) => {
      label = "Totale vaccinati";
      let y;
      y = s.territori.filter(x => x.nome_territorio === territory_name)[0].totale_vaccinati;
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
    [...storico_vaccini].forEach((s, i) => {
      label = "Dosi Disponibili";
      let y;
      y = s.territori.filter(x => x.nome_territorio === territory_name)[0].totale_dosi_consegnate;
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
    [...storico_vaccini].forEach((s, i) => {
      label = "Vaccinati oggi";
      let y;
      y = s.territori.filter(x => x.nome_territorio === territory_name)[0].nuovi_vaccinati;
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
    [...storico_vaccini].forEach((s, i) => {
      label = "Percentuale vaccinata";
      let y;
      y = s.territori.filter(x => x.nome_territorio === territory_name)[0].percentuale_popolazione_vaccinata;
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
    old_chart.update();
    return old_chart;
  } else {

    let ctx = $("canvas#italia")[0].getContext('2d');
    chart = new Chart(ctx, {
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
    return chart;
  }
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
  } else if (order === 4) {
    vaccini.territori.sort((a, b) => a.percentuale_dosi_utilizzate > b.percentuale_dosi_utilizzate ? 1 : -1);
  }

  if (reverse) {
    vaccini.territori.reverse();
  }

  // fill table
  $("table#territori tbody").html("");

  vaccini.territori.forEach((t, i) => {
    if (t.nome_territorio != "Italia") {
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

      let new_tr = `<tr id="${t.codice_territorio}" class="territorio">`;
      new_tr += `<td><span class="mobile">${nome_territorio_corto}</span><span class="pc">${t.nome_territorio}</span></td>`;
      new_tr += `<td>${t.totale_vaccinati}`;
      new_tr += `<td>${percentuale_vaccinati}</td>`;
      new_tr += `<td>${t.totale_dosi_consegnate}`;
      new_tr += `<td>${percentuale_dosi}`;
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
    if (sort_by_name) {
      vaccini.territori.sort((a, b) => a.nome_territorio > b.nome_territorio ? 1 : -1);
    }
    data = [...vaccini.territori].filter(x => x.nome_territorio != "Italia").map(x => x.totale_vaccinati);
    background_colors = data.map(x => `hsla(${x / Math.max(...data) * 120}, 100%, 50%, 0.5)`);
    border_colors = data.map(x => `hsl(${x / Math.max(...data) * 120}, 100%, 50%)`);
    hover_background_colors = data.map(x => `hsla(${x / Math.max(...data) * 120}, 100%, 50%, 0.25)`);
    labels = [...vaccini.territori].filter(x => x.nome_territorio != "Italia").map(x => x.nome_territorio);
    label = "Totale vaccinati";
  } else if (order === 1) {
    vaccini.territori.sort((a, b) => a.percentuale_popolazione_vaccinata > b.percentuale_popolazione_vaccinata ? 1 : -1);
    if (sort_by_name) {
      vaccini.territori.sort((a, b) => a.nome_territorio > b.nome_territorio ? 1 : -1);
    }
    data = [...vaccini.territori].filter(x => x.nome_territorio != "Italia").map(x => parseFloat(x.percentuale_popolazione_vaccinata).toFixed(2));
    labels = [...vaccini.territori].filter(x => x.nome_territorio != "Italia").map(x => x.nome_territorio);
    background_colors = data.map(x => `hsla(${x / 100 * 120}, 100%, 50%, 0.5)`);
    border_colors = data.map(x => `hsl(${x / 100 * 120}, 100%, 50%)`);
    hover_background_colors = data.map(x => `hsla(${x / 100 * 120}, 100%, 50%, 0.25)`);
    label = "Percentuale popolazione vaccinata";
  } else if (order === 2) {
    vaccini.territori.sort((a, b) => a.totale_dosi_consegnate > b.totale_dosi_consegnate ? 1 : -1);
    if (sort_by_name) {
      vaccini.territori.sort((a, b) => a.nome_territorio > b.nome_territorio ? 1 : -1);
    }
    data = [...vaccini.territori].filter(x => x.nome_territorio != "Italia").map(x => x.totale_dosi_consegnate);
    background_colors = data.map(x => `hsla(${x / Math.max(...data) * 120}, 100%, 50%, 0.5)`);
    border_colors = data.map(x => `hsl(${x / Math.max(...data) * 120}, 100%, 50%)`);
    hover_background_colors = data.map(x => `hsla(${x / Math.max(...data) * 120}, 100%, 50%, 0.25)`);
    labels = [...vaccini.territori].filter(x => x.nome_territorio != "Italia").map(x => x.nome_territorio);
    label = "Totale dosi di vaccino consegnate";
  } else if (order === 3) {
    vaccini.territori.sort((a, b) => a.percentuale_dosi_utilizzate > b.percentuale_dosi_utilizzate ? 1 : -1);
    if (sort_by_name) {
      vaccini.territori.sort((a, b) => a.nome_territorio > b.nome_territorio ? 1 : -1);
    }
    data = [...vaccini.territori].filter(x => x.nome_territorio != "Italia").map(x => x.percentuale_dosi_utilizzate.toFixed(2));
    background_colors = data.map(x => `hsla(${120 - x / 100 * 120}, 100%, 50%, 0.5)`);
    border_colors = data.map(x => `hsl(${120 - x / Math.max(...data) * 120}, 100%, 50%)`);
    hover_background_colors = data.map(x => `hsla(${120 - x /100 * 120}, 100%, 50%, 0.25)`);
    labels = [...vaccini.territori].filter(x => x.nome_territorio != "Italia").map(x => x.nome_territorio);
    label = "Percentuale vaccini utlizzati";
  }

  // calculate average
  let average = data.reduce((sum, d) => parseFloat(sum) + parseFloat(d)) / data.length;
  if (average > 100) average = parseInt(average);

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
        backgroundColor: "rgba(0, 0, 0, 0)",
        borderColor: "hsl(0, 100%, 50%)",
        pointRadius: 0,
        borderWidth: 1
      }],
    };
    old_chart.update();
    return old_chart;
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
          backgroundColor: "rgba(0, 0, 0, 0)",
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
    return chart;
  }
};



const load_variations = (order, reverse) => {
  // sort data
  if (order === 0) {
    vaccini.territori.sort((a, b) => a.nome_territorio > b.nome_territorio ? 1 : -1);
  } else if (order === 1) {
    vaccini.territori.sort((a, b) => a.nuovi_vaccinati > b.nuovi_vaccinati ? 1 : -1);
  } else if (order === 2) {
    vaccini.territori.sort((a, b) => a.percentuale_nuovi_vaccinati > b.percentuale_nuovi_vaccinati ? 1 : -1);
  } else if (order === 3) {
    vaccini.territori.sort((a, b) => a.nuove_dosi_consegnate > b.nuove_dosi_consegnate ? 1 : -1);
  } else if (order === 4) {
    vaccini.territori.sort((a, b) => a.percentuale_nuove_dosi_consegnate > b.percentuale_nuove_dosi_consegnate ? 1 : -1);
  }

  if (reverse) {
    vaccini.territori.reverse();
  }

  // fill table
  $("table#variazioni tbody").html("");

  vaccini.territori.forEach((t, i) => {
    if (t.nome_territorio != "Italia") {

      let nome_territorio_corto;
      if (t.codice_territorio === "06") {
        nome_territorio_corto = "E.R.";
      } else if (t.codice_territorio === "07") {
        nome_territorio_corto = "F.V.G";
      }

      let nuovi_vaccinati;
      let percentuale_nuovi_vaccinati;
      if (t.nuovi_vaccinati === undefined) {
        nuovi_vaccinati = 0;
        percentuale_nuovi_vaccinati = 0;
      } else {
        nuovi_vaccinati = t.nuovi_vaccinati;
        percentuale_nuovi_vaccinati = t.percentuale_nuovi_vaccinati;
      }

      let nuove_dosi;
      let nuove_dosi_percentuale;
      if (t.nuove_dosi_consegnate === undefined) {
        nuove_dosi = 0;
        nuove_dosi_percentuale = 0;
      } else {
        nuove_dosi = t.nuove_dosi_consegnate;
        nuove_dosi_percentuale = t.percentuale_nuove_dosi_consegnate;
      }

      let new_tr = `<tr id="${t.codice_territorio}" class="territorio">`;
      if (nome_territorio_corto) {
        new_tr += `<td><span class="pc">${t.nome_territorio}</span><span class="mobile">${nome_territorio_corto}</span></td>`;
      } else {
        new_tr += `<td>${t.nome_territorio}</td>`;
      }

      new_tr += `<td>+${nuovi_vaccinati}`;
      new_tr += `<td>+${percentuale_nuovi_vaccinati.toFixed(2)}%</td>`;
      new_tr += `<td>+${nuove_dosi}`;
      new_tr += `<td>+${nuove_dosi_percentuale.toFixed(2)}%</td>`;
      new_tr += "</tr>";
      $("table#variazioni tbody").append(new_tr);
    }
  });
};


const load_variations_chart = (order, sort_by_name, old_chart) => {
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
    vaccini.territori.sort((a, b) => a.nuovi_vaccinati > b.nuovi_vaccinati ? 1 : -1);
    if (sort_by_name) {
      vaccini.territori.sort((a, b) => a.nome_territorio > b.nome_territorio ? 1 : -1);
    }
    data = [...vaccini.territori].filter(x => x.nome_territorio != "Italia").map(x => x.nuovi_vaccinati);
    label = "Nuovi vaccinati";
  } else if (order === 1) {
    vaccini.territori.sort((a, b) => a.percentuale_nuovi_vaccinati > b.percentuale_nuovi_vaccinati ? 1 : -1);
    if (sort_by_name) {
      vaccini.territori.sort((a, b) => a.nome_territorio > b.nome_territorio ? 1 : -1);
    }
    data = [...vaccini.territori].filter(x => x.nome_territorio != "Italia").map(x => x.percentuale_nuovi_vaccinati.toFixed(2));
    label = "Variazione nuovi vaccinati";
  } else if (order === 2) {
    vaccini.territori.sort((a, b) => a.nuove_dosi_consegnate > b.nuove_dosi_consegnate ? 1 : -1);
    if (sort_by_name) {
      vaccini.territori.sort((a, b) => a.nome_territorio > b.nome_territorio ? 1 : -1);
    }
    data = [...vaccini.territori].filter(x => x.nome_territorio != "Italia").map(x => x.nuove_dosi_consegnate);
    label = "Nuovi vaccini";
  } else if (order === 3) {
    vaccini.territori.sort((a, b) => a.percentuale_nuove_dosi_consegnate > b.percentuale_nuove_dosi_consegnate ? 1 : -1);
    if (sort_by_name) {
      vaccini.territori.sort((a, b) => a.nome_territorio > b.nome_territorio ? 1 : -1);
    }
    data = [...vaccini.territori].filter(x => x.nome_territorio != "Italia").map(x => x.percentuale_nuove_dosi_consegnate.toFixed(2));
    label = "Variazione nuovi vaccini";
  }

  background_colors = data.map(x => `hsla(${x / Math.max(...data) * 120}, 100%, 50%, 0.5)`);
  border_colors = data.map(x => `hsl(${x / Math.max(...data) * 120}, 100%, 50%)`);
  hover_background_colors = data.map(x => `hsla(${x / Math.max(...data) * 120}, 100%, 50%, 0.25)`);
  labels = [...vaccini.territori].filter(x => x.nome_territorio != "Italia").map(x => x.nome_territorio);

  // calculate average
  let average = data.reduce((sum, d) => parseFloat(sum) + parseFloat(d)) / data.length;
  if (average > 100) average = parseInt(average);

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
        backgroundColor: "hsla(0, 100%, 50%, 0.5)",
        borderColor: "hsl(0, 100%, 50%)",
        pointRadius: 0,
        borderWidth: 1
      }],
    };
    old_chart.update();
    return old_chart;
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
            backgroundColor: "hsla(0, 100%, 50%, 0.5)",
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
    return chart;
  }
};


// load data about each category
const load_categories = (order, reverse) => {
  if (order === 0) {
    vaccini.categorie.sort((a, b) => a.id_categoria > b.id_categoria ? 1 : -1);
  } else if (order === 1) {
    vaccini.categorie.sort((a, b) => a.totale_vaccinati > b.totale_vaccinati ? 1 : -1);
  } else if (order === 2) {
    vaccini.categorie.sort((a, b) => a.nuovi_vaccinati > b.nuovi_vaccinati ? 1 : -1);
  } else if (order === 3) {
    vaccini.categorie.sort((a, b) => a.percentuale_nuovi_vaccinati > b.percentuale_nuovi_vaccinati ? 1 : -1);
  }

  if (reverse) {
    vaccini.categorie.reverse();
  }

  $("table#categorie tbody").html("");

  vaccini.categorie.forEach((t, i) => {
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
    return old_chart;
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
    return chart;
  }
};


// load data about each gender
const load_genders = (order, reverse) => {
  if (order === 0) {
    vaccini.sesso.sort((a, b) => a.nome_categoria > b.nome_categoria ? 1 : -1);
  } else if (order === 1) {
    vaccini.sesso.sort((a, b) => a.totale_vaccinati > b.totale_vaccinati ? 1 : -1);
  } else if (order === 2) {
    vaccini.sesso.sort((a, b) => a.nuovi_vaccinati > b.nuovi_vaccinati ? 1 : -1);
  } else if (order === 3) {
    vaccini.sesso.sort((a, b) => a.percentuale_nuovi_vaccinati > b.percentuale_nuovi_vaccinati ? 1 : -1);
  }

  if (reverse) {
    vaccini.sesso.reverse();
  }

  $("table#sesso tbody").html("");

  vaccini.sesso.forEach((t, i) => {
    let nuovi_vaccinati;
    let percentuale_nuovi_vaccinati;
    if (t.nuovi_vaccinati === undefined) {
      nuovi_vaccinati = 0;
      percentuale_nuovi_vaccinati = 0;
    } else {
      nuovi_vaccinati = t.nuovi_vaccinati;
      percentuale_nuovi_vaccinati = t.percentuale_nuovi_vaccinati;
    }

    let new_tr = `<tr id="${t.nome_categoria}" class="sesso">`;
    new_tr += `<td>${t.nome_categoria}</td>`;
    new_tr += `<td>${t.totale_vaccinati}</td>`;
    new_tr += `<td>+${nuovi_vaccinati}</td>`;
    new_tr += `<td>+${percentuale_nuovi_vaccinati.toFixed(2)}%</td>`;
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
};


// load data about age ranges
const load_age_ranges = (order, reverse) => {
  if (order === 0) {
    vaccini.fasce_eta.sort((a, b) => a.nome_categoria > b.nome_categoria ? 1 : -1);
  } else if (order === 1) {
    vaccini.fasce_eta.sort((a, b) => a.totale_vaccinati > b.totale_vaccinati ? 1 : -1);
  } else if (order === 2) {
    vaccini.fasce_eta.sort((a, b) => a.nuovi_vaccinati > b.nuovi_vaccinati ? 1 : -1);
  } else if (order === 3) {
    vaccini.fasce_eta.sort((a, b) => a.percentuale_nuovi_vaccinati > b.percentuale_nuovi_vaccinati ? 1 : -1);
  }

  if (reverse) {
    vaccini.fasce_eta.reverse();
  }

  $("table#fasce_eta tbody").html("");

  vaccini.fasce_eta.forEach((t, i) => {
    let nuovi_vaccinati;
    let percentuale_nuovi_vaccinati;
    if (t.nuovi_vaccinati == undefined) {
      nuovi_vaccinati = 0;
      percentuale_nuovi_vaccinati = 0;
    } else {
      nuovi_vaccinati = t.nuovi_vaccinati;
      percentuale_nuovi_vaccinati = t.percentuale_nuovi_vaccinati;
    }

    let new_tr = `<tr id="${t.nome_categoria}" class="territorio">`;
    new_tr += `<td>${t.nome_categoria}</td>`;
    new_tr += `<td>${t.totale_vaccinati}</td>`;
    new_tr += `<td>+${nuovi_vaccinati}</td>`;
    new_tr += `<td>+${percentuale_nuovi_vaccinati.toFixed(2)}%</td>`;
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
    return old_chart;
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
    return chart;
  }
};


// main function
$(document).ready(() => {
  // load basic infos
  set_last_update();
  load_selection();
  load_italy();
  // load tables
  load_territories(0, false);
  load_variations(0, false);
  load_categories(0, false);
  load_genders(0, false);
  load_age_ranges(0, false);

  // load charts and keep the variable
  let italy_chart = load_italy_chart([0, 1]);
  let territories_chart = load_territories_chart(0, false);
  let variations_chart = load_variations_chart(0, false);
  let categories_chart = load_categories_chart(0);
  let genders_chart = load_genders_chart(0);
  let ages_ranges_chart = load_age_ranges_chart(0);

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
      load_territories(column, reverse);
    } else if (table_id === "variazioni") {
      load_variations(column, reverse);
    } else if (table_id === "categorie") {
      load_categories(column, reverse);
    } else if (table_id === "sesso") {
      load_genders(column, reverse);
    } else if (table_id === "fasce_eta") {
      load_age_ranges(column, reverse);
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
