"""Build a scratch lab from the locally installed Pedestrian Elevator example."""

from copy import deepcopy
from itertools import count

from lxml import etree as xml


class Starter:
    def __init__(self, tree):
        self.ids = count(max(int(n) for n in tree.xpath(".//Id/text()") if n.isdecimal()) + 1)

    @staticmethod
    def set(node, path, val):
        field = node.find(path)
        if field is None:
            field = xml.SubElement(node, path)
        field.text = xml.CDATA(str(val))

    def clone(self, template, group, name, x=None, y=None):
        copy = deepcopy(template)
        for identity in copy.xpath(".//Id"):
            identity.text = str(next(self.ids))
        self.set(copy, "Name", name)
        if x is not None:
            copy.find("X").text = str(x)
            copy.find("Y").text = str(y)
        group.append(copy)
        return copy

    def param(self, block, name, code, unit=None):
        item = block.find(f'Parameters/Parameter[Name="{name}"]')
        value = item.find("Value")
        if value is not None:
            item.remove(value)
        value = xml.SubElement(item, "Value", Class="CodeUnitValue" if unit else "CodeValue")
        self.set(value, "Code", code)
        if unit:
            xml.SubElement(value, "Unit", Class=unit[0]).text = xml.CDATA(unit[1])

    @staticmethod
    def points(shape, coords, z=False):
        pts = shape.find("Points")
        pts.clear()
        for x, y in coords:
            item = xml.SubElement(pts, "Point")
            xml.SubElement(item, "X").text = str(x)
            xml.SubElement(item, "Y").text = str(y)
            if z:
                xml.SubElement(item, "Z").text = "0"

    def rect(self, template, group, name, x, y, width, height, color):
        node = self.clone(template, group, name, x, y)
        for tag, text in {"Width": width, "Height": height, "FillColor": color,
                          "ZHeight": 0, "DrawMode": "SHAPE_DRAW_2D"}.items():
            node.find(tag).text = str(text)
        return node

    def variable(self, template, group, name, typ, initial, y):
        node = self.clone(template, group, name, 720, y)
        self.set(node, "Properties/Type", typ)
        self.set(node, "Properties/InitialValue/Code", initial)

    def function(self, template, group, name, parameters, body, y):
        node = self.clone(template, group, name, 1000, y)
        for current in node.findall("Parameter"):
            node.remove(current)
        anchor = node.find("Body")
        for pname, typ in parameters:
            p = xml.Element("Parameter")
            self.set(p, "Name", pname)
            self.set(p, "Type", typ)
            anchor.addprevious(p)
        self.set(node, "Body", body)


def named(container, name):
    elem = container.find(f'*[Name="{name}"]')
    if elem is None:
        raise ValueError(f"Missing {name}. Use the installed Pedestrian Elevator example for AnyLogic 8.9.")
    return elem


def clear(node):
    for element in list(node):
        node.remove(element)


def drop(node, tag):
    child = node.find(tag)
    if child is not None:
        node.remove(child)


def make_seed(tree):
    writer = Starter(tree)
    model = tree.find("Model")
    original_package = model.findtext("JavaPackageName")
    if original_package != "pedestrian_elevator":
        raise ValueError("Expected the official Pedestrian Elevator example")
    agents = model.find("ActiveObjectClasses")
    main = named(agents, "Main")
    student = named(agents, "Pedestrian")
    levels = main.find("Presentation")
    first = named(levels, "first_floor")
    second = named(levels, "second_floor")
    interface = named(levels, "auxiliaryLevel")
    first_items = first.find("Presentation")
    interface_items = interface.find("Presentation")
    wall, line, elevator = (deepcopy(first_items.find(tag)) for tag in ("Wall", "TargetLine", "Elevator"))
    top_group = named(interface_items, "panelGroup").find("Presentation")
    rect, text = (deepcopy(top_group.find(tag)) for tag in ("Rectangle", "Text"))
    population_visual = deepcopy(interface_items.find("EmbeddedObjectPresentation"))

    variables = main.find("Variables")
    functions = main.find("Functions")
    variable = deepcopy(variables.find('Variable[@Class="PlainVariable"]'))
    function = deepcopy(named(functions, "setLevelsVisibility"))
    areas = main.find("Areas")
    dashboard = deepcopy(named(areas, "view2D"))
    objects = main.find("EmbeddedObjects")
    source, lift, walk, sink, population = (
        deepcopy(named(objects, n)) for n in ("pedSource", "pedElevator", "toExit", "pedSink", "pedestrians")
    )
    links = main.find("Connectors")
    connector = deepcopy(links.find("Connector"))
    package = "anylogic_lab_seed"
    drop(model, "ModelResources")
    for group in (variables, functions, areas, objects, links, interface_items):
        clear(group)
    for level in list(levels.findall("Level")):
        if level not in (first, second, interface):
            levels.remove(level)
    for node, name in ((first,"floor1"),(second,"floor2"),(interface,"interfaceLevel"),(student,"Student")):
        writer.set(node,"Name",name)
    main.find("ScaleRuler/Scale").text = "20"
    main.find("ScaleRuler/ModelLength").text = "5"
    model.find("Frame/Width").text = "570"
    model.find("Frame/Height").text = "320"
    clear(student.find("Variables"))
    drop(student,"StartupCode")
    drop(student,"Functions")
    student_items = student.find("Presentation/Level/Presentation")
    dot = deepcopy(student_items.find("Oval"))
    clear(student_items)
    dot.find("RadiusX").text = dot.find("RadiusY").text = "4"
    writer.set(dot,"Name","studentDot")
    student_items.append(dot)
    for i,(name,typ,initial) in enumerate((
        ("originFloor","int","-1"), ("destinationFloor","int","-1"),
        ("waitStartedAt","double","-1"), ("boardedAt","double","-1"),
    )):
        writer.variable(variable,student.find("Variables"),name,typ,initial,70+26*i)

    for i,level in enumerate((first,second),1):
        level.find("Z").text = str((i-1)*72)
        items = level.find("Presentation")
        clear(items)
        writer.rect(rect,items,f"corridor{i}",30,76,490,190,-1182472)
        writer.rect(rect,items,f"lobby{i}",125,141,326,61,-1642506)
        wall_node = writer.clone(wall,items,f"walls{i}",30,76)
        wall_node.find("Closed").text = "true"
        wall_node.find("FillingType").text = "NO_FILL"
        writer.points(wall_node,[(0,0),(0,25),(25,0),(490,0),(465,0),(490,25),
            (490,190),(490,165),(465,190),(0,190),(25,190),(0,165)],True)
        for port,x in (("entry",52),("exit",498)):
            target = writer.clone(line,items,f"{port}{i}",x,195)
            writer.points(target,[(0,0),(0,50)])
        nameplate = writer.clone(text,items,f"lobbyLabel{i}",242,145)
        writer.set(nameplate,"Text","Elevator lobby")
        nameplate.find("Font/Size").text = "13"
        nameplate.find("Color").text = "-12500957"
        for j,letter in enumerate("ABC"):
            cx=171+112*j
            writer.rect(rect,items,f"shaftBay{letter}{i}",cx-31,83,62,56,-2104086)
            plate=writer.clone(text,items,f"bayLabel{letter}{i}",cx-4,90)
            writer.set(plate,"Text",letter)
            plate.find("Font/Size").text = "12"
            plate.find("Color").text = "-12500957"
            if i==1:
                car=writer.clone(elevator,items,f"lift{letter}",cx,111)
                car.find("Rotation").text = "0"
                car.find("DrawShaft").text = "false"
                car.find("Width/Value").text = "3.1"
                car.find("Depth/Value").text = "2.8"
                car.find("CabinHeight/Value").text = "2.5"
                desc=car.find("EmbeddedObject")
                writer.param(desc,"capacity","4")
                writer.param(desc,"movementMode","ElevatorMovementMode.ELEVATOR_MOVEMENT_BY_TIME_PER_LEVEL")
                writer.param(desc,"timePerLevel","4",("TimeUnits","SECOND"))
                writer.param(desc,"minStayTime","7",("TimeUnits","SECOND"))
                writer.param(desc,"allLevels","false")
                writer.param(desc,"levels","{ floor1, floor2 }")

    interface_items.append(population_visual)
    for i in (1,2):
        click = f"showFloor({i-1});"
        b=writer.rect(rect,interface_items,f"floorButton{i}",32+48*(i-1),24,40,29,-1971758)
        txt=writer.clone(text,interface_items,f"floorButtonText{i}",42+48*(i-1),30)
        writer.set(txt,"Text",f"{i}F")
        txt.find("Font/Size").text = "14"
        txt.find("Color").text = "-12500957"
        writer.set(b,"OnClickCode",click)
        writer.set(txt,"OnClickCode",click)
    view=writer.clone(dashboard,areas,"dashboard",0,0)
    view.find("Width").text="570"
    view.find("Height").text="320"

    clear(population.find("Parameters"))
    writer.set(population,"Name","students")
    population.find("X").text="900"
    population.find("Y").text="325"
    objects.append(population)
    blocks=("arrivals","ride","walkToExit","leaveBuilding")
    types=("PedSource","PedElevator","PedGoTo","PedSink")
    xs=(730,850,970,1090)
    for idx,letter in enumerate("ABC"):
        y=105+65*idx
        arrival, ride, walker, _ = (
            writer.clone(t,objects,n+letter,x,y) for t,n,x in zip((source,lift,walk,sink),blocks,xs)
        )
        clear(arrival.find('Parameters/Parameter[Name="newPed"]/Value/EntityEmbeddedObject/Parameters'))
        writer.param(arrival,"rate","studentsPerMinutePerLift",("RateUnits","PER_MINUTE"))
        writer.param(arrival,"locationLine","entryLines[uniform_discr(0, 1)]")
        writer.param(arrival,"population","students")
        writer.param(arrival,"onExit","assignTrip(ped);")
        writer.param(ride,"elevator",f"lift{letter}")
        writer.param(ride,"targetLevel","floors[ped.destinationFloor]")
        writer.param(ride,"onStartWaiting","startWaiting(ped);")
        writer.param(ride,"onEnterElevator",f"""board(ped);
int load = ++currentLoadByCar[{idx}];
if (load > lift{letter}.getCapacity()) throw new IllegalStateException("Cabin exceeded capacity");
peakLoadByCar[{idx}] = Math.max(peakLoadByCar[{idx}], load);""")
        writer.param(ride,"onExitElevator",f"""alight(ped, level);
if (--currentLoadByCar[{idx}] < 0) throw new IllegalStateException("Cabin load became negative");""")
        writer.param(walker,"locationLine","exitLines[ped.destinationFloor]")
        for j in range(1,4):
            wire=writer.clone(connector,links,f"link{letter}{j}",xs[j]-20,y)
            for side,ix in (("Source",j),("Target",j-1)):
                writer.set(wire,side+"EmbeddedObjectReference/ItemName",blocks[ix]+letter)
                writer.set(wire,side+"ConnectableItemReference/ClassName",types[ix])
            writer.points(wire,[(0,0),(-80,0)])

    for i,(name,typ,initial) in enumerate((
        ("studentsPerMinutePerLift","double","10.0"),
        ("floors","Level[]","null"), ("entryLines","TargetLine[]","null"), ("exitLines","TargetLine[]","null"),
        ("visibleFloor","int","0"), ("waitingByFloor","int[]","new int[2]"),
        ("currentLoadByCar","int[]","new int[3]"), ("peakLoadByCar","int[]","new int[3]"),
        ("boardedCount","int","0"), ("transportedCount","int","0"),
        ("waitSeconds","double","0.0"), ("rideSeconds","double","0.0"),
    )):
        writer.variable(variable,variables,name,typ,initial,370+26*i)
    for i,(name,args,body) in enumerate((
        ("showFloor",[("index","int")], """visibleFloor = index;
for (int i = 0; i < floors.length; i++) floors[i].setVisible(i == index);"""),
        ("assignTrip",[("ped","Student")], """ped.originFloor = java.util.Arrays.asList(floors).indexOf(ped.getLevel());
if (ped.originFloor < 0) throw new IllegalStateException("Unknown pedestrian level");
ped.destinationFloor = 1 - ped.originFloor;"""),
        ("startWaiting",[("ped","Student")], """ped.waitStartedAt = time();
waitingByFloor[ped.originFloor]++;"""),
        ("board",[("ped","Student")], """ped.boardedAt = time();
if (ped.waitStartedAt >= 0) {
    waitSeconds += ped.boardedAt - ped.waitStartedAt;
    waitingByFloor[ped.originFloor]--;
}
boardedCount++;"""),
        ("alight",[("ped","Student"),("level","Level")], """if (level != floors[ped.destinationFloor] || ped.boardedAt < 0)
    throw new IllegalStateException("Passenger left at the wrong level");
rideSeconds += time() - ped.boardedAt;
transportedCount++;"""),
    )):
        writer.function(function,functions,name,args,body,370+30*i)
    writer.set(main,"StartupCode","""floors = new Level[] { floor1, floor2 };
entryLines = new TargetLine[] { entry1, entry2 };
exitLines = new TargetLine[] { exit1, exit2 };
showFloor(0);
dashboard.navigateTo();""")

    experiment=model.find("Experiments/SimulationExperiment")
    clear(experiment.find("Presentation"))
    experiment.find("BypassInitialScreen").text="true"
    writer.set(experiment.find("PresentationProperties"),"ExecutionMode","virtualTime")
    for e in (experiment,model.find("RunConfiguration")):
        writer.set(e.find("ModelTimeProperties"),"StopOption","Stop at specified time")
        writer.set(e.find("ModelTimeProperties"),"FinalTime","360.0")
    config=model.find("RunConfiguration/AnimationProperties/StopNever")
    if config is not None:
        config.text="false"
    for item in tree.xpath(".//PackageName"):
        if item.text==original_package:
            item.text=xml.CDATA(package)
    for item in tree.xpath(".//ClassName[text()='Pedestrian']"):
        item.text=xml.CDATA("Student")
    writer.set(model,"JavaPackageName",package)
    writer.set(model,"Description","Local two-floor pedestrian lab")
    return tree
