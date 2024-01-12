#!/bin/bash

echo "************************************************************" \
    && echo "    Environment: $ENVIRONMENT" \
    && echo "    Service Name: $SERVICE" \
    && echo "    Branch Name: $BRANCH_NAME" \
    && echo "    Commit SHA: $COMMIT_HASH" \
    && echo "    Build Date: $BUILD_DATE" \
    && echo "************************************************************" \
    && python3 app.py