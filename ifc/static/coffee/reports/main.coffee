successColorHex = "#5cb85c"
dangerColorHex = '#d9534f'


showAttendance = (data) ->
  startAngleOffset = Math.PI

  arcGen = d3.arc()
    .outerRadius 150
    .innerRadius 90
    .startAngle startAngleOffset

  container = d3.select('#attendance')
  container.select('.loading').remove()

  svg = container.append('svg')
    .attr 'width', 400
    .attr 'height', 400

  group = svg.append('g')
    .attr "transform", "translate(200,200)"

  # draw the red arc
  group.append('path')
    .attr 'd', arcGen.endAngle startAngleOffset + 2 * Math.PI
    .attr 'class', 'attendanceArc'
    .attr 'fill', dangerColorHex
    .attr 'stroke', 'black'

  # draw the green arc
  group.append('path')
    .attr 'd', arcGen.endAngle startAngleOffset + (Math.PI * 2 * data.attendance)
    .attr 'class', 'attendanceArc'
    .attr 'fill', successColorHex
    .attr 'stroke', 'black'

  group.append('text')
    .attr 'transform', 'translate(-40, 15)'
    .attr 'font-size', '3.1em'
    .text "#{Math.floor(data.attendance * 100)}%"

  document.getElementById('attendance-total').innerText = data.total_guests


showHostGuestAttendance = (data) ->
  hostData = {}
  hostData[d[0]] = {'attended': d[1]} for d in data.host_attendance_normalized
  hostData[d[0]]['listed'] = d[1] for d in data.host_attendance_raw

  orderedHosts = Object.keys(hostData).sort (a, b) ->
    hostData[b].attended - hostData[a].attended


  makeTable = () ->
    table = document.createElement('table')
    table.id = 'att-table'
    table.classList.add('table')
    table.classList.add('table-hover')

    thead = document.createElement('thead')
    theadRow = document.createElement('tr')
    nameTh = document.createElement('th')
    nameTh.innerText = 'Name'
    theadRow.appendChild(nameTh)
    ratioTh = document.createElement('th')
    ratioTh.innerText = 'Percent attendance (total attended)'
    theadRow.appendChild(ratioTh)
    thead.appendChild(theadRow)
    table.appendChild(thead)

    table.appendChild(makeTbody())
    table


  makeTbody = (page=1, perPage=5, hosts=orderedHosts) ->
    pagedHostNames = hosts.slice((page-1)*perPage, (page*perPage))
    tbody = document.createElement('tbody')
    tbody.id = 'att-tbody'

    for host in pagedHostNames
      tr = document.createElement('tr')
      name = document.createElement('td')
      name.innerText = host
      tr.appendChild(name)
      ratio = document.createElement('td')
      ratio.innerText = "#{Math.round(hostData[host]['attended']*100)}% (#{hostData[host]['listed']})"
      ratio.classList.add('text-right')
      tr.appendChild(ratio)
      tbody.appendChild(tr)

    tbody


  makePages = () ->
    paginationElt = document.getElementsByClassName('pagination')[0]
    numPages = Math.ceil(orderedHosts.length/5)
    for page in [0..numPages-1]
      pElt = document.createElement('li')
      pElt.classList.add('att-pg')
      pElt.setAttribute('data-page', page + 1)
      pElt.addEventListener 'click', (e) ->
        document.querySelectorAll('li.att-pg.active')[0].classList.remove('active')
        @classList.add('active')
        newBody = makeTbody @getAttribute('data-page')
        document.getElementById('att-tbody').remove()
        document.getElementById('att-table').appendChild(newBody)
      pAElt = document.createElement('a')
      pAElt.href = 'javascript:void(0)'
      pAElt.innerText = page + 1
      pElt.appendChild(pAElt)
      if page == 0
        pElt.classList.add 'active'
      paginationElt.appendChild(pElt)


  attendanceTable = document.getElementById('host-attendance')
  attendanceTable.getElementsByClassName('loading')[0].remove()
  attendanceTable.appendChild(makeTable())
  makePages()

'''
showPopulationChart = (data) ->
  updatePopulationFooter = (datum) ->
    timeElt = document.getElementById('pop-time')
    guestElt = document.getElementById('pop-guests')
    timeString = (new Date(datum.time)).toLocaleTimeString()
    timeElt.innerText = timeString
    guestElt.innerText = datum.population

  container = d3.select('#population-chart')
  container.select('.loading').remove()

  svg = container.append('svg')
    .attr 'width', 800
    .attr 'height', 400
    .attr 'class', 'pop-chart'

  maxYVal = Math.ceil(d3.max(data.population, (d) ->
    d.population) * 1.3)
  y = d3.scaleLinear()
    .domain [0, maxYVal]
    .range [400, 0]
  x = d3.scaleLinear()
    .domain [0, data.population.length - 1]
    .range [0, 800]

  xAxis = d3.axisBottom().scale(x)

  svg.append 'g'
    .attr 'transform', 'translate(0, 360)'
    .call xAxis

  lineFunc = d3.line()
    .x((d, i) -> x(i))
    .y((d) -> y(d.population))
    .curve d3.curveBundle.beta(0.95)

  svg.append 'path'
    .attr 'd', lineFunc(data.population)
    .attr 'stroke', 'steelblue'
    .attr 'stroke-width', 2
    .attr 'fill', 'none'

  vertical = d3.select '.pop-chart'
    .append 'line'
    .attr 'stroke', '#bbb'
    .attr 'stroke-width', '1'
    .attr 'x1', 0
    .attr 'x2', 0
    .attr 'y1', 0
    .attr 'y2', 400

  d3.select(".pop-chart")
    .on("mousemove", () ->
      mousex = d3.mouse(this)
      mousex = mousex[0]
      index = Math.floor(x.invert(mousex))
      datum = data.population[index]
      vertical.attr 'x1', mousex
        .attr 'x2', mousex
      updatePopulationFooter datum
      d3.select(this)
        .classed("hover", true)
        .attr("stroke", '#ddd')
        .attr("stroke-width", "0.5px"))
    .on("mouseenter", () ->
      mousex = d3.mouse(this)
      mousex = mousex[0]
      vertical.attr 'x1', mousex
        .attr('x2', mousex))
'''

showPopulationChart = (data) =>
  ctx = document.getElementById("myChart")

  male_population = data.gender_population.male
  female_population = data.gender_population.female
  buckets = data.population

  max = Math.max.apply(Math, (b.population for b in buckets))

  chart = new Chart(ctx, {
    type: 'line'
    data: {
      labels: ((new Date(bucket.time)).toTimeString() for bucket in buckets)
      datasets: [
        {
          label: 'Total'
          data: (bucket.population for bucket in buckets)
          fill: false
          pointHitRadius: 15
          borderColor: 'rgb(75, 75, 75)'
          lineTension: 0.1
        },
        {
          label: 'Guys'
          data: (bucket.population for bucket in male_population)
          fill: true
          pointHitRadius: 15
          backgroundColor: 'rgba(91, 109, 227, 0.5)'
          borderColor: 'rgb(91, 109, 227)'
          lineTension: 0.1
        },
        {
          label: 'Girls'
          data: (bucket.population for bucket in female_population)
          fill: true
          pointHitRadius: 15
          backgroundColor: 'rgba(200, 91, 227, 0.5)'
          borderColor: 'rgb(200, 91, 227)'
          lineTension: 0.1
        },
      ]
    }
    options:
      scales:
        yAxes: [{
          ticks:
            max: Math.ceil(max * 1.2)
            beginAtZero: true
        }]
  })

$.get('report/data').done((res) ->
  showAttendance res
  showHostGuestAttendance res
  showPopulationChart res
)
