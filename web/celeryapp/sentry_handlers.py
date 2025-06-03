"""
Sentry handlers for Celery task monitoring.
"""

import sentry_sdk
from celery import signals
from django.conf import settings


@signals.task_prerun.connect
def sentry_task_prerun(
    sender=None, task_id=None, task=None, args=None, kwargs=None, **kw
):
    """Start a Sentry transaction for Celery tasks."""
    if not hasattr(settings, "SENTRY_DSN") or not settings.SENTRY_DSN:
        return

    # Start a new transaction for this task
    transaction = sentry_sdk.start_transaction(
        name=task.name,
        op="celery.task",
    )

    # Store transaction on task instance for later use
    task.request.sentry_transaction = transaction
    transaction.set_tag("task.id", task_id)
    transaction.set_tag("task.name", task.name)

    # Add breadcrumb
    sentry_sdk.add_breadcrumb(
        message=f"Task {task.name} started",
        category="celery",
        level="info",
        data={
            "task_id": task_id,
            "args": str(args)[:200],  # Limit size
            "kwargs": str(kwargs)[:200],  # Limit size
        },
    )


@signals.task_postrun.connect
def sentry_task_postrun(
    sender=None,
    task_id=None,
    task=None,
    args=None,
    kwargs=None,
    retval=None,
    state=None,
    **kw,
):
    """Finish the Sentry transaction for Celery tasks."""
    if not hasattr(settings, "SENTRY_DSN") or not settings.SENTRY_DSN:
        return

    # Get transaction from task instance
    transaction = getattr(task.request, "sentry_transaction", None)
    if transaction:
        transaction.set_tag("task.state", state)
        transaction.set_status("ok" if state == "SUCCESS" else "internal_error")
        transaction.finish()

    # Add breadcrumb
    sentry_sdk.add_breadcrumb(
        message=f"Task {task.name} completed",
        category="celery",
        level="info" if state == "SUCCESS" else "warning",
        data={
            "task_id": task_id,
            "state": state,
            "runtime": getattr(task.request, "runtime", None),
        },
    )


@signals.task_failure.connect
def sentry_task_failure(
    sender=None,
    task_id=None,
    exception=None,
    args=None,
    kwargs=None,
    traceback=None,
    einfo=None,
    **kw,
):
    """Capture Celery task failures to Sentry."""
    if not hasattr(settings, "SENTRY_DSN") or not settings.SENTRY_DSN:
        return

    # The exception will be automatically captured by Celery integration
    # We just add additional context here
    with sentry_sdk.configure_scope() as scope:
        scope.set_tag("task.id", task_id)
        scope.set_tag("task.name", sender.name)
        scope.set_context(
            "celery_task",
            {
                "task_id": task_id,
                "task_name": sender.name,
                "args": str(args)[:500],
                "kwargs": str(kwargs)[:500],
            },
        )

    # Add breadcrumb
    sentry_sdk.add_breadcrumb(
        message=f"Task {sender.name} failed",
        category="celery",
        level="error",
        data={
            "task_id": task_id,
            "exception": str(exception),
        },
    )


@signals.task_retry.connect
def sentry_task_retry(sender=None, task_id=None, reason=None, einfo=None, **kw):
    """Log Celery task retries to Sentry."""
    if not hasattr(settings, "SENTRY_DSN") or not settings.SENTRY_DSN:
        return

    # Add breadcrumb
    sentry_sdk.add_breadcrumb(
        message=f"Task {sender.name} retried",
        category="celery",
        level="warning",
        data={
            "task_id": task_id,
            "reason": str(reason),
            "retry_count": getattr(sender.request, "retries", 0),
        },
    )
