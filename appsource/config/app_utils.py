

import datetime
import sys
from django.db.models import Q
from config import settings
from config import app_logger
logger = app_logger.createLogger("app")


def user_login_check(user):
    if user.is_active and user.is_authenticated:
        return True
    else:
        return False


def convert_date_time_format(date_time, tz_offset=0, date_format=None):
    if date_time:
        return date_time.strftime("{}".format(settings.DEFAULT_DATE_TIME_FORMAT))
    else:
        return ""


def convert_date_format(date):
    if date:
        return date.strftime("{}".format(settings.DEFAULT_DATE_FORMAT))
    else:
        return date


def convert_time_format(time):
    return time.strftime("{}".format(settings.DEFAULT_TIME_FORMAT))


def ordering(request, qs):
    order = list()
    try:
        if request.method == "POST":
            pDict = request.POST.copy()
        else:
            pDict = request.GET.copy()

        sorting_cols = 0
        sort_key = 'order[{0}][column]'.format(sorting_cols)
        while sort_key in pDict:
            sorting_cols += 1
            sort_key = 'order[{0}][column]'.format(sorting_cols)

        col_data = extract_datatables_column_data(request)
        order_columns = list()
        for col in col_data:
            order_columns.append(col['name'])

        for i in range(sorting_cols):
            sort_dir = 'asc'
            try:
                sort_col = int(pDict.get('order[{0}][column]'.format(i)))
                sort_dir = pDict.get('order[{0}][dir]'.format(i))
            except ValueError:
                sort_col = 0
            sdir = '-' if sort_dir == 'desc' else ''

            sortcol = order_columns[sort_col]
            if sortcol:
                if isinstance(sortcol, list):
                    for sc in sortcol:
                        order.append('{0}{1}'.format(
                            sdir, sc.replace('.', '__')))
                else:
                    order.append('{0}{1}'.format(
                        sdir, sortcol.replace('.', '__')))
        if order and not isinstance(qs, list):
            return qs.order_by(*order)
        else:
            if order:
                order = order[0].split("-")
                if len(order) > 1:
                    qs.sort(key=lambda k: k[order[1]], reverse=True)
                else:
                    qs.sort(key=lambda k: k[order[0]])
    except Exception as e:
        app_logger.exceptionlogs(e)
    return qs


def extract_datatables_column_data(request):
    col_data = list()
    try:
        if request.method == "POST":
            request_dict = request.POST.copy()
        else:
            request_dict = request.GET.copy()
        counter = 0
        data_name_key = 'columns[{0}][name]'.format(counter)

        while data_name_key in request_dict:
            searchable = True if request_dict.get(
                'columns[{0}][searchable]'.format(counter)) == 'true' else False
            orderable = True if request_dict.get(
                'columns[{0}][orderable]'.format(counter)) == 'true' else False

            col_data.append({'name': request_dict.get(data_name_key),
                             'data': request_dict.get('columns[{0}][data]'.format(counter)),
                             'searchable': searchable,
                             'orderable': orderable,
                             'search.value': request_dict.get('columns[{0}][search][value]'.format(counter)),
                             'search.regex': request_dict.get('columns[{0}][search][regex]'.format(counter)),
                             })
            counter += 1
            data_name_key = 'columns[{0}][name]'.format(counter)

    except Exception as e:
        app_logger.exceptionlogs(e)
    return col_data


def search(request, qs, column_list, is_download, admin_user_search):
    try:
        if request.method == "POST":
            pDict = request.POST.copy()
        else:
            pDict = request.GET.copy()
        if request.session.has_key('search_value') and is_download:
            search = request.session.get('search_value')
        else:
            search = pDict.get(u'search[value]', None)
        if search:  # if search term exists only - go inside
            if column_list and is_download:
                col_data = column_list
            else:
                col_data = extract_datatables_column_data(request)
            if not isinstance(qs, list):
                q = Q()
                fk_list = [field.name for field in qs.model._meta.fields if field.get_internal_type() in [
                    "ForeignKey", "OneToOneField"]]
                for col_no, col in enumerate(col_data):
                    if col['name'] in fk_list:
                        col['name'] = "%s.name" % (col['name'])
                    if col['name'] == "action":
                        col['searchable'] = False

                    if search and col['searchable'] and col_data[col_no]['name'] != '':
                        q |= Q(
                            **{'{0}__icontains'.format(col_data[col_no]['name'].replace('.', '__')): search})
                    if not is_download:
                        if col['search.value'] and col_data[col_no]['name'] != '':
                            qs = qs.filter(
                                **{'{0}__icontains'.format(col_data[col_no]['name'].replace('.', '__')): col['search.value']})
                qs = qs.filter(q)
            else:
                final_qs = list()
                for row in qs:
                    for key, value in row.iteritems():
                        row_value = row[key]
                        if isinstance(row_value, (str, unicode)):
                            if row_value.lower().find(search.lower()) != -1:
                                final_qs.append(row)
                                break
                            # if row_value.lower().startswith(search.lower()):
                            #     final_qs.append(row)
                            #     break
                qs = final_qs

    except Exception as e:
        app_logger.exceptionlogs(e)
        qs = list()
    return qs



def paging(request, qs):
    try:
        if request.method == "POST":
            pDict = request.POST.copy()
        else:
            pDict = request.GET.copy()

        # default max rows is 500 hardcoded
        limit = min(int(pDict.get(u'length', -1)), 500)
        start = int(pDict.get(u'start', 0))

        if limit == -1:
            return qs

        offset = start + limit
        return qs[start:offset]

    except Exception as e:
        app_logger.exceptionlogs(e)
    return qs


def method_for_datatable_operations(request, qs, order=True, is_download=False, column_list=list(), admin_user_search=False):
    total_records = 0
    total_display_records = 0
    try:
        if isinstance(qs, list):
            total_records = len(qs)
        else:
            try:
                total_records = qs.count()
            except:
                total_records = len(qs)
        qs = search(request, qs, column_list, is_download, admin_user_search)
        if isinstance(qs, list):
            total_display_records = len(qs)
        else:
            try:
                total_display_records = qs.count()
            except:
                total_records = len(qs)
        if order:
            qs = ordering(request, qs)
        if not is_download:
            qs = paging(request, qs)
    except Exception as e:
        app_logger.exceptionlogs(e)
    return qs, total_records, total_display_records


def final_dict(request, total_records, total_display_records, result_data):
    ret = dict()
    try:
        pDict = request.POST.copy()
        draw = int(pDict.get('draw', 0))
        ret = {
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': total_display_records,
            'data': result_data,
            'result': 'ok',
        }

    except Exception as e:
        app_logger.exceptionlogs(e)
    return ret


@app_logger.functionlogs(log="app")
def convert_html_to_pdf(request, context, template_name):          
    try:
        from wkhtmltopdf.views import PDFTemplateResponse
        response = PDFTemplateResponse(
            request=request, 
            context=context, 
            template=template_name,
            cmd_options={
                'encoding': 'utf8',
                'quiet': None,
                'disable-javascript':'',
                'enable-local-file-access': True,
                
            },
            # footer_template="pdf/footer.html"
        )
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' %(exc_traceback.tb_lineno, e))      
    return response



def num2word(num):
    try:
        d = { 0 : 'zero', 1 : 'one', 2 : 'two', 3 : 'three', 4 : 'four', 5 : 'five',
            6 : 'six', 7 : 'seven', 8 : 'eight', 9 : 'nine', 10 : 'ten',
            11 : 'eleven', 12 : 'twelve', 13 : 'thirteen', 14 : 'fourteen',
            15 : 'fifteen', 16 : 'sixteen', 17 : 'seventeen', 18 : 'eighteen',
            19 : 'nineteen', 20 : 'twenty',
            30 : 'thirty', 40 : 'forty', 50 : 'fifty', 60 : 'sixty',
            70 : 'seventy', 80 : 'eighty', 90 : 'ninety' }
        k = 1000
        tk = k*10
        l = k*100
        tl = l*10
        c = l*100
        
        if not(isinstance(num, int)) or (num < 0):
            raise Exception('Make sure that, the number you passed "'+str(num)+'" doesn\'t contain any alphabet or special symbol!')

        assert(0 <= num)

        if (num < 20):
            return d[num]

        if (num < 100):
            if num % 10 == 0: return d[num]
            else: return d[num // 10 * 10] + '-' + d[num % 10]

        if (num < k):
            if num % 100 == 0: return d[num // 100] + ' hundred'
            else: return d[num // 100] + ' hundred and ' + num2word(num % 100)

        if (num >= k and num < l):
            if num % k == 0: return num2word(num // k) + ' thousand'
            else: return num2word(num // k) + ' thousand, ' + num2word(num % k)

        if (num >= l and num < c):
            if (num % l) == 0: return num2word(num // l) + ' lakh'
            else: return num2word(num // l) + ' lakh, ' + num2word(num % l)

        if (num >= c):
            if num % c == 0: return num2word(num // c) + ' crore'
            else: return num2word(num // c) + ' crore, ' + num2word(num % c)
        
        raise AssertionError('num is too large: %s' % str(num))
    except Exception as e:
        app_logger.exceptionlogs(e)
    return None
