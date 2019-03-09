import json

from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


class Seat:
    def __init__(self, stations, seat_no):
        self.seat_no = seat_no
        self.no_stations = stations
        self.busy_stations = [False] * stations

    def verify_if_free(self, start, end):
        for i in range(start, end):
            if self.busy_stations[i]:
                return True
        return False

    def set_busy(self, start, end):
        for i in range(start, end):
            self.busy_stations[i] = True

    def __str__(self):
        return str(self.seat_no)


class Compartment:
    def __init__(self, no_seats, comp_no):
        self.comp_no = comp_no
        self.free_places = no_seats
        self.no_seats = no_seats
        self.seats = []
        for i in range(no_seats):
            self.seats.append(Seat(6, self.comp_no * 8 + i + 1))

    def verify_free_seats(self, no, start, end):
        no_seats_to_verify = no
        list = []
        for i in self.seats:
            busy = i.verify_if_free(start, end)
            if busy is False:
                list.append(i)
                no_seats_to_verify = no_seats_to_verify - 1
                if no_seats_to_verify == 0:
                    return list

        if no_seats_to_verify != 0:
            return []

    def __str__(self):
        return str(self.comp_no + 1)


class Carriage:
    def __init__(self, no_compartments, carriage_no):
        self.carriage_no = carriage_no
        self.no_compartments = no_compartments
        self.compartments = []
        for i in range(no_compartments):
            self.compartments.append(Compartment(8, i))

    def free_places(self):
        no = 0
        for x in self.compartments:
            no = no + x.free_places
        return no

    def __str__(self):
        return str(self.carriage_no)


class Train:
    def __init__(self, no_carriages):
        self.no_carriages = no_carriages
        self.carriages = []
        for i in range(no_carriages):
            self.carriages.append(Carriage(10, i + 1))


train = Train(1)
listTickets = [[[5], [2, 3], [4, 1], [2, 2, 1], [2, 1, 1, 1], [1, 1, 1, 1, 1]],
               [[4], [2, 2], [3, 1], [2, 1, 1], [1, 1, 1, 1]], [[3], [2, 1], [1, 1, 1]], [[2], [1, 1]], [[1]]]




@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/buy', methods=['POST'])
def split():
    try:
        data = json.loads(request.data)
    except Exception:
        return jsonify({'success': False})

    nr_tickets = data['numberOfPersons']
    start = data['start']
    end = data['end']
    ok = True
    index = 0
    tI = 5 - nr_tickets
    seatDict = []

    for listPossibilities in listTickets[tI]:
        ok = True
        for tickets in listPossibilities:
            if buy(tickets, start, end) is not False:
                best_carriage, sets_list = buy(tickets, start, end)
                dictVal = {
                    'carriage': best_carriage,
                    'seats': sets_list
                }
                seatDict.append(dictVal)
                print("Here")
            else:
                seatDict = []
                ok = False
                break
            if ok == True:
                break

    for value in seatDict:
        print(value)
        for key, val in value.items():
            if key == 'carriage':
                print(val)
            else:
                for i in val:
                    print(i)

    return ""


def buy(tickets, start, end):
    # nr_tickets = request.form['nr_tickets']
    # start = request.form['start']
    # end = request.form['end']
    nr_tickets = 4
    start = 2
    end = 4

    if (nr_tickets < 1 or nr_tickets > 5):
        return jsonify({
            'status': 'error',
            'message': 'To many tickets!'
        })

    best_carriage = -1
    min_seats = 10
    best_compartment = -1
    sets_list = []
    for carriage in train.carriages:
        for compartment in carriage.compartments:
            if compartment.free_places >= nr_tickets:
                list = compartment.verify_free_seats(nr_tickets, start, end)
                if len(list) > 0:
                    if min_seats > (8 - compartment.free_places) + nr_tickets:
                        min_seats = (8 - compartment.free_places) + nr_tickets
                        best_compartment = compartment
                        best_carriage = carriage
                        sets_list = list

    if len(sets_list) > 0:
        for seat in sets_list:
            seat.set_busy(start, end)
        best_compartment.free_places -= nr_tickets
        return best_carriage, sets_list

    return False


if __name__ == '__main__':
    app.run()
