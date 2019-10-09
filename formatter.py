from logstash_async.formatter import LogstashFormatter


class AuditLogFormatter(LogstashFormatter):

    def _get_extra_fields(self, record):
        # don't use the default extra fields, those only pollute our logs
        return {}

    def format(self, record):
        # override format() because we don't want the extra fields added by the LogstashFormatter
        message = {
            '@timestamp': self._format_timestamp(record.created),
            '@version': '1',
            'message': record.getMessage(),
        }

        if self._tags:
            message['tags'] = self._tags

        # record fields
        record_fields = self._get_record_fields(record)
        message.update(record_fields)

        # prepare dynamic extra fields
        extra_fields = self._get_extra_fields(record)

        # wrap extra fields in configurable namespace
        if self._extra_prefix:
            message[self._extra_prefix] = extra_fields
        else:
            message.update(extra_fields)

        # move existing extra record fields into the configured prefix
        self._move_extra_record_fields_to_prefix(message)

        return self._serialize(message)
