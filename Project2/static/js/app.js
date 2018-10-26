
function buildMap() {
  var lrmap = L.map('map').setView([15.5994, -28.6731], 2);
  L.tileLayer('https://api.tiles.mapbox.com/v4/mapbox.dark/{z}/{x}/{y}.png?access_token=pk.eyJ1Ijoic2hhbWVldGhhIiwiYSI6ImNqbjExdjczaTI1Y3czcG5vaDVvZHVqcnYifQ.XgXeLUf_4pa8v6UmZDo_Iw')
  .addTo(lrmap);
  // var url = "/maps";
  // console.log( '{{ data }}' )
  d3.json("../static/data/top_100.json", function(response) {
    var data = response;
    console.log(data);
    var migrationLayer = new L.migrationLayer({
      map: lrmap,
      data: data,
      pulseRadius:30,
      pulseBorderWidth:3,
      arcWidth:1,
      arcLabel:true,
      arcLabelFont:'10px sans-serif',
    }
    );
    migrationLayer.addTo(lrmap);


    function getColor(d) {
      return d > 12500000 ? '#e41a1c' :
            d > 2500000  ? '#377eb8' :
            d > 1350000  ? '#4daf4a' :
            d > 1000000  ? '#984ea3' :
            d > 750000   ? '#ff7f00' :
            d > 600000   ? '#ffff33' :
                       '#a65628';

    }
        // Set up the legend
        var legend = L.control({
          position: "bottomleft"
        });
        legend.onAdd = function() {
          var div = L.DomUtil.create("div", "info legend");
          var limits = [0, 600000, 750000, 1000000, 1350000, 2500000, 12500000];
          var colors = ['#a65628', '#ffff33', '#ff7f00', '#984ea3', '#4daf4a', '#377eb8', '#e41a1c'];
          var labels = []

          for (var i = 0; i < limits.length; i++) {
        div.innerHTML +=
            '<i style="background:' + getColor(limits[i] + 1) + '"></i> ' +
            limits[i] + (limits[i + 1] ? '&ndash;' + limits[i + 1] + '<br>' : '+');
    }

    return div;
  };

  // Add legend to the map
  legend.addTo(lrmap);
});
}

buildMap();



